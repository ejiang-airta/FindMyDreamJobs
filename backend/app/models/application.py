from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.database.connection import Base

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    resume_id = Column(Integer, ForeignKey("resumes.id"), nullable=False)
    application_url = Column(String)
    application_status = Column(String)  # e.g. In Progress, Rejected, Offered
    applied_date = Column(DateTime)
