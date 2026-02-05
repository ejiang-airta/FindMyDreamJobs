# File: backend/app/models/user_integration.py
# OAuth token storage for external integrations (Gmail, etc.)
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from app.database.connection import Base
from datetime import datetime, timezone
import uuid


class UserIntegration(Base):
    __tablename__ = "user_integrations"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    provider = Column(String(50), nullable=False)            # e.g. "gmail"
    scopes = Column(JSONB, nullable=True)                    # e.g. ["gmail.readonly"]
    refresh_token_enc = Column(Text, nullable=False)         # Fernet-encrypted refresh token
    access_token_enc = Column(Text, nullable=True)           # Fernet-encrypted access token
    expires_at = Column(DateTime, nullable=True)             # Access token expiry
    status = Column(String(20), default="active", nullable=False)  # active | revoked | error
    last_sync_at = Column(DateTime, nullable=True)           # Last successful Gmail scan

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc), nullable=True)

    # Unique constraint: one integration per provider per user
    __table_args__ = (
        UniqueConstraint("user_id", "provider", name="uq_user_integration_provider"),
    )

    # Relationships
    user = relationship("User", backref="integrations")
