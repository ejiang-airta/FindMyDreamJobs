# File: backend/app/models/jdi_candidate.py
# Staging table for JDI-extracted job candidates
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Index, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from app.database.connection import Base
from datetime import datetime, timezone
import uuid


class JDICandidate(Base):
    __tablename__ = "jdi_candidates"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    source = Column(String(50), nullable=False)              # linkedin | indeed | trueup | other
    source_message_id = Column(String, nullable=True)        # Gmail message ID
    job_url_raw = Column(Text, nullable=True)                # Original URL from email
    job_url_canonical = Column(Text, nullable=True)          # Dedupe key (cleaned URL)
    title = Column(Text, nullable=True)
    company = Column(Text, nullable=True)
    location = Column(Text, nullable=True)
    employment_type = Column(Text, nullable=True)
    salary_text = Column(Text, nullable=True)
    jd_text = Column(Text, nullable=True)                    # Full job description
    jd_hash = Column(String(64), nullable=True)              # SHA-256 of jd_text for quick dedupe
    jd_extraction_confidence = Column(Integer, nullable=True)  # 0-100
    match_score = Column(Integer, nullable=True)             # 0-100
    match_reasons = Column(JSONB, nullable=True)             # 2-4 bullet strings
    selected_resume_id = Column(Integer, ForeignKey("resumes.id"), nullable=True)
    status = Column(String(20), default="new", nullable=False)  # new | ignored | promoted
    seen_at = Column(DateTime, nullable=True)                # Read/unread tracking

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc), nullable=True)

    __table_args__ = (
        # Unique active candidate per user per canonical URL
        UniqueConstraint("user_id", "job_url_canonical", name="uq_jdi_user_job_url"),
        # Feed query: filter by status, sort by score
        Index("ix_jdi_user_status_score", "user_id", "status", "match_score"),
        # Unread tracking
        Index("ix_jdi_user_seen", "user_id", "seen_at"),
    )

    # Relationships
    user = relationship("User", backref="jdi_candidates")
    selected_resume = relationship("Resume", foreign_keys=[selected_resume_id])
