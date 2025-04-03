from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database.connection import Base
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import JSONB


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # ✅ ADD ONLY THIS
    job_title = Column(String, nullable=False)
    company_name = Column(String, nullable=False)
    location = Column(String, nullable=True)
    job_description = Column(Text, nullable=False)  # 🛑 Change from String → Text for large JD content
    job_link = Column(String, nullable=True)
    extracted_skills = Column(JSONB, nullable=True)  # ✅ Store as an 2D array /w skills/frequency
    required_experience = Column(String, nullable=True) # ✅ Adding this for tracking experienve
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=True)


    # Define the relationship between the Job and Application models
    applications = relationship("Application", back_populates="job")
    job_matches = relationship("JobMatch", back_populates="job")
    user = relationship("User", back_populates="jobs")  # ✅ Optional, but nice to have
