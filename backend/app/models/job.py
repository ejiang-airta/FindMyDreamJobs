from sqlalchemy import Column, Integer, String, DateTime, Text
from app.database.connection import Base
from datetime import datetime, timezone
from sqlalchemy.orm import relationship

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    job_title = Column(String, nullable=False)
    company_name = Column(String, nullable=False)
    location = Column(String, nullable=True)
    job_description = Column(Text, nullable=False)  # 🛑 Change from String → Text for large JD content
    job_url = Column(String, nullable=True)
    extracted_skills = Column(Text, nullable=True)  # ✅ Adding this back
    posted_at = Column(DateTime, nullable=True)
    added_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Define the relationship between the Job and Application models
    applications = relationship("Application", back_populates="job")
    job_matches = relationship("JobMatch", back_populates="job")
