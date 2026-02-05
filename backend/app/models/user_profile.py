# File: backend/app/models/user_profile.py
# JDI (Job Daily Intelligence) user preferences
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from app.database.connection import Base
from datetime import datetime, timezone


class UserProfile(Base):
    __tablename__ = "user_profiles"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    target_titles = Column(JSONB, nullable=True)            # e.g. ["Software Engineer", "Backend Developer"]
    target_locations = Column(JSONB, nullable=True)          # e.g. ["Toronto, ON", "Remote"]
    jdi_min_score = Column(Integer, default=60, nullable=False)
    jdi_sources_enabled = Column(JSONB, nullable=True)       # e.g. ["linkedin", "indeed", "trueup"]
    jdi_base_resume_ids = Column(JSONB, nullable=True)       # JSON array of resume IDs, max 3
    jdi_resume_select_mode = Column(String(20), default="auto_best", nullable=False)  # auto_best | keyword_rules
    jdi_resume_keyword_rules = Column(JSONB, nullable=True)  # keyword → resume_id mapping rules
    jdi_scan_window_days = Column(Integer, default=7, nullable=False)  # 1-7 days for email scan
    jdi_custom_source_patterns = Column(JSONB, nullable=True)  # custom email patterns for "others"

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc), nullable=True)

    # Relationships
    user = relationship("User", backref="profile", uselist=False)
