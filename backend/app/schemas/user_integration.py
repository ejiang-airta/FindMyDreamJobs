# File: backend/app/schemas/user_integration.py
# Pydantic schemas for user integration (Gmail OAuth) status
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class IntegrationStatusOut(BaseModel):
    """Public-facing integration status (no tokens exposed)."""
    id: str
    user_id: int
    provider: str
    status: str                          # active | revoked | error
    scopes: Optional[list[str]] = None
    last_sync_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class IntegrationConnectOut(BaseModel):
    """Response from initiating OAuth flow."""
    authorization_url: str


class IntegrationCallbackIn(BaseModel):
    """OAuth callback query parameters."""
    code: str
    state: Optional[str] = None
