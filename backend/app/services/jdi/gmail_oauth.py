# File: backend/app/services/jdi/gmail_oauth.py
# Google OAuth flow for Gmail integration
import os
import json
import base64
import logging
from datetime import datetime, timezone, timedelta
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from sqlalchemy.orm import Session

from app.models.user_integration import UserIntegration
from app.services.jdi.encryption import encrypt_token, decrypt_token

logger = logging.getLogger(__name__)

# OAuth configuration — constants
GMAIL_SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def _get_oauth_config():
    """Read OAuth config from env at call time (after load_dotenv has run)."""
    client_id = os.getenv("GOOGLE_CLIENT_ID", "")
    client_secret = os.getenv("GOOGLE_CLIENT_SECRET", "")
    redirect_uri = os.getenv(
        "JDI_OAUTH_REDIRECT_URI",
        "http://localhost:8000/api/integrations/gmail/callback",
    )
    return client_id, client_secret, redirect_uri


def _build_client_config() -> dict:
    """Build the OAuth client config dict from env vars."""
    client_id, client_secret, redirect_uri = _get_oauth_config()
    return {
        "web": {
            "client_id": client_id,
            "client_secret": client_secret,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": [redirect_uri],
        }
    }


def encode_state(user_id: int, frontend_url: str) -> str:
    """Encode user_id + frontend_url into a base64 JSON state string."""
    payload = json.dumps({"uid": user_id, "fu": frontend_url})
    return base64.urlsafe_b64encode(payload.encode()).decode()


def decode_state(state: str) -> tuple:
    """
    Decode the OAuth state string back to (user_id, frontend_url).
    Falls back gracefully if state is in the old plain-integer format.
    """
    try:
        payload = json.loads(base64.urlsafe_b64decode(state.encode()).decode())
        return int(payload["uid"]), payload["fu"]
    except Exception:
        # Legacy fallback: state was just a plain user_id string
        fallback_url = os.getenv("FRONTEND_BASE_URL", "http://localhost:3000")
        return int(state), fallback_url


def get_authorization_url(user_id: int, frontend_url: str) -> str:
    """
    Generate the Google OAuth consent URL.
    Both user_id and frontend_url are embedded in the state param so the
    callback knows where to redirect regardless of which backend handles it
    (important: Google's registered redirect_uri always points to the
    production backend, so preview environments share that callback).
    """
    _, _, redirect_uri = _get_oauth_config()
    flow = Flow.from_client_config(
        _build_client_config(),
        scopes=GMAIL_SCOPES,
        redirect_uri=redirect_uri,
    )
    authorization_url, _state = flow.authorization_url(
        access_type="offline",       # Get a refresh token
        include_granted_scopes="true",
        prompt="consent",            # Force consent to always get refresh_token
        state=encode_state(user_id, frontend_url),
    )
    return authorization_url


def handle_oauth_callback(code: str, user_id: int, db: Session) -> UserIntegration:
    """
    Exchange the authorization code for tokens, encrypt, and store.
    Returns the created/updated UserIntegration record.
    """
    _, _, redirect_uri = _get_oauth_config()
    flow = Flow.from_client_config(
        _build_client_config(),
        scopes=GMAIL_SCOPES,
        redirect_uri=redirect_uri,
    )
    flow.fetch_token(code=code)
    credentials = flow.credentials

    # Encrypt tokens
    refresh_enc = encrypt_token(credentials.refresh_token) if credentials.refresh_token else None
    access_enc = encrypt_token(credentials.token) if credentials.token else None
    expires_at = credentials.expiry if credentials.expiry else None

    # Upsert: check for existing integration
    integration = (
        db.query(UserIntegration)
        .filter_by(user_id=user_id, provider="gmail")
        .first()
    )

    if integration:
        # Update existing
        if refresh_enc:
            integration.refresh_token_enc = refresh_enc
        integration.access_token_enc = access_enc
        integration.expires_at = expires_at
        integration.status = "active"
        integration.scopes = GMAIL_SCOPES
    else:
        # Create new
        if not refresh_enc:
            raise ValueError("No refresh token received from Google. Re-authorize with prompt=consent.")
        integration = UserIntegration(
            user_id=user_id,
            provider="gmail",
            scopes=GMAIL_SCOPES,
            refresh_token_enc=refresh_enc,
            access_token_enc=access_enc,
            expires_at=expires_at,
            status="active",
        )
        db.add(integration)

    db.commit()
    db.refresh(integration)
    logger.info(f"Gmail integration saved for user_id={user_id}")
    return integration


def get_gmail_credentials(user_id: int, db: Session) -> Credentials:
    """
    Load stored tokens for a user, refresh if expired, and return
    a google.oauth2.credentials.Credentials object ready for API calls.
    """
    integration = (
        db.query(UserIntegration)
        .filter_by(user_id=user_id, provider="gmail", status="active")
        .first()
    )
    if not integration:
        raise ValueError(f"No active Gmail integration for user_id={user_id}")

    refresh_token = decrypt_token(integration.refresh_token_enc)
    access_token = decrypt_token(integration.access_token_enc) if integration.access_token_enc else None

    client_id, client_secret, _ = _get_oauth_config()
    creds = Credentials(
        token=access_token,
        refresh_token=refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=client_id,
        client_secret=client_secret,
        scopes=GMAIL_SCOPES,
    )

    # Set expiry if we have it
    if integration.expires_at:
        creds.expiry = integration.expires_at

    # Auto-refresh if expired
    if creds.expired and creds.refresh_token:
        logger.info(f"Refreshing Gmail access token for user_id={user_id}")
        creds.refresh(Request())

        # Store refreshed token
        integration.access_token_enc = encrypt_token(creds.token)
        integration.expires_at = creds.expiry
        db.commit()

    return creds


def revoke_integration(user_id: int, db: Session) -> bool:
    """
    Revoke Gmail integration: mark as revoked.
    Optionally could also call Google's revoke endpoint.
    """
    integration = (
        db.query(UserIntegration)
        .filter_by(user_id=user_id, provider="gmail")
        .first()
    )
    if not integration:
        return False

    integration.status = "revoked"
    db.commit()
    logger.info(f"Gmail integration revoked for user_id={user_id}")
    return True
