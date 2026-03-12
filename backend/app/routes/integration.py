# File: backend/app/routes/integration.py
# API routes for Gmail OAuth integration (JDI)
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.database.connection import SessionLocal
from app.models.user_integration import UserIntegration
from app.schemas.user_integration import IntegrationStatusOut, IntegrationConnectOut
from app.services.jdi.gmail_oauth import (
    get_authorization_url,
    handle_oauth_callback,
    revoke_integration,
    decode_state,
)
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/integrations", tags=["Integrations"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/gmail/connect", response_model=IntegrationConnectOut)
def gmail_connect(
    user_id: int = Query(...),
    frontend_url: str = Query(..., description="Origin URL of the frontend (window.location.origin)"),
    db: Session = Depends(get_db),
):
    """
    Initiate Gmail OAuth flow.
    frontend_url is passed by the browser so the callback knows which frontend
    to redirect back to — essential for preview environments where the Google
    registered redirect_uri always points to the production backend.
    Returns the Google consent URL that the frontend should redirect the user to.
    """
    try:
        auth_url = get_authorization_url(user_id, frontend_url)
        return IntegrationConnectOut(authorization_url=auth_url)
    except Exception as e:
        logger.error(f"Failed to generate Gmail auth URL: {e}")
        raise HTTPException(status_code=500, detail="Failed to initiate Gmail connection")


@router.get("/gmail/callback")
def gmail_callback(
    code: str = Query(...),
    state: str = Query(...),  # base64 JSON: {uid, fu} — see gmail_oauth.encode_state()
    db: Session = Depends(get_db),
):
    """
    Handle Google OAuth callback.
    Exchanges the authorization code for tokens, encrypts, and stores them.
    Redirects the user directly to /settings?jdi_connected=true on their frontend
    (works for both production and preview environments).
    """
    try:
        user_id, frontend_url = decode_state(state)
    except (ValueError, TypeError):
        raise HTTPException(status_code=400, detail="Invalid state parameter")

    try:
        handle_oauth_callback(code=code, user_id=user_id, db=db)
        # Redirect directly to /settings#jdi (where JDISection lives) with success flag.
        # The #jdi hash ensures the Job Intel tab is active on arrival.
        # Bypasses the /jdi/setup redirect shim, avoiding an extra Protected wrapper hop.
        redirect_url = f"{frontend_url}/settings?jdi_connected=true#jdi"
        return RedirectResponse(url=redirect_url, status_code=302)
    except ValueError as e:
        logger.error(f"OAuth callback error: {e}")
        error_redirect = f"{frontend_url}/settings?jdi_error=true#jdi"
        return RedirectResponse(url=error_redirect, status_code=302)
    except Exception as e:
        logger.error(f"OAuth callback unexpected error: {e}")
        error_redirect = f"{frontend_url}/settings?jdi_error=true#jdi"
        return RedirectResponse(url=error_redirect, status_code=302)


@router.post("/gmail/revoke")
def gmail_revoke(user_id: int = Query(...), db: Session = Depends(get_db)):
    """
    Revoke Gmail integration for a user.
    Marks the integration as revoked (tokens remain encrypted but inactive).
    """
    success = revoke_integration(user_id=user_id, db=db)
    if not success:
        raise HTTPException(status_code=404, detail="No Gmail integration found")
    return {"status": "revoked", "provider": "gmail"}


@router.get("/gmail/status", response_model=IntegrationStatusOut)
def gmail_status(user_id: int = Query(...), db: Session = Depends(get_db)):
    """
    Get the current Gmail integration status for a user.
    """
    integration = (
        db.query(UserIntegration)
        .filter_by(user_id=user_id, provider="gmail")
        .first()
    )
    if not integration:
        raise HTTPException(status_code=404, detail="No Gmail integration found")
    return integration
