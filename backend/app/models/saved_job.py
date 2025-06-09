# This file defines the SavedJob model for the application.
# File: /backend/app/models/saved_job.py

# File: app/models/saved_job.py

from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.schema import UniqueConstraint
from datetime import datetime, timezone
import uuid
from app.database.connection import Base  # ✅ Use shared Base for Alembic to recognize it

class SavedJob(Base):
    __tablename__ = "saved_jobs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    

    search_id = Column(String, nullable=False)  # from job["job_id"]

    job_title = Column(String, nullable=False)
    employer_name = Column(String, nullable=False)
    employer_logo = Column(String)
    employer_website = Column(String)
    job_location = Column(String)
    job_is_remote = Column(Boolean, default=False)
    job_employment_type = Column(String)
    job_salary = Column(String, nullable=True)
    job_description = Column(Text, nullable=True)
    job_apply_link = Column(String, nullable=False)  # from job["job_google_link"]
    job_posted_at = Column(DateTime, nullable=False)  # from job["job_posted_at_datetime_utc"]
    saved_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Define this argument to ensure that the search_id + user_id combination is unique:
    __table_args__ = (
        UniqueConstraint('user_id', 'search_id', name='uq_user_search'),
    )

    # Put relationship mappings after all column + constraint definitions
    user = relationship("User", back_populates="saved_jobs")
