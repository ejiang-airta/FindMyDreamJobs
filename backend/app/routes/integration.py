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
)
import logging
import os

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/integrations", tags=["Integrations"])

# Frontend redirect URL after OAuth callback
FRONTEND_BASE_URL = os.getenv("FRONTEND_BASE_URL", "http://localhost:3000")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/gmail/connect", response_model=IntegrationConnectOut)
def gmail_connect(user_id: int = Query(...), db: Session = Depends(get_db)):
    """
    Initiate Gmail OAuth flow.
    Returns the Google consent URL that the frontend should redirect the user to.
    """
    try:
        auth_url = get_authorization_url(user_id)
        return IntegrationConnectOut(authorization_url=auth_url)
    except Exception as e:
        logger.error(f"Failed to generate Gmail auth URL: {e}")
        raise HTTPException(status_code=500, detail="Failed to initiate Gmail connection")


@router.get("/gmail/callback")
def gmail_callback(
    code: str = Query(...),
    state: str = Query(...),  # Contains user_id
    db: Session = Depends(get_db),
):
    """
    Handle Google OAuth callback.
    Exchanges the authorization code for tokens, encrypts, and stores them.
    Redirects user back to the frontend JDI setup page.
    """
    try:
        user_id = int(state)
    except (ValueError, TypeError):
        raise HTTPException(status_code=400, detail="Invalid state parameter")

    try:
        integration = handle_oauth_callback(code=code, user_id=user_id, db=db)
        # Redirect back to frontend JDI setup page with success flag
        redirect_url = f"{FRONTEND_BASE_URL}/jdi/setup?jdi_connected=true"
        return RedirectResponse(url=redirect_url, status_code=302)
    except ValueError as e:
        logger.error(f"OAuth callback error: {e}")
        # Redirect to frontend with error flag
        error_redirect = f"{FRONTEND_BASE_URL}/jdi/setup?jdi_error=true"
        return RedirectResponse(url=error_redirect, status_code=302)
    except Exception as e:
        logger.error(f"OAuth callback unexpected error: {e}")
        # Redirect to frontend with error flag
        error_redirect = f"{FRONTEND_BASE_URL}/jdi/setup?jdi_error=true"
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
