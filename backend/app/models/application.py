from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database.connection import Base
from datetime import datetime, timezone

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    resume_id = Column(Integer, ForeignKey("resumes.id"), nullable=False)
    application_url = Column(String)
    application_status = Column(String)  # e.g. In Progress, Rejected, Offered
    applied_date = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)  # ✅ Replace created_at with applied_date
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=True)

    # Define the relationship between the Application and User models
    user = relationship("User", back_populates="applications")  # ✅ Track which user applied for a job
    job = relationship("Job", back_populates="applications")  # ✅ Link each application to a job posting
    resume = relationship("Resume", back_populates="applications")  # ✅ Track which resume was used