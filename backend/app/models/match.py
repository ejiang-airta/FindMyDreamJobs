from sqlalchemy import Column, Integer, ForeignKey, Float, Text, DateTime
from sqlalchemy.orm import relationship
from app.database.connection import Base
from datetime import datetime, timezone

class JobMatch(Base):
    __tablename__ = "job_matches"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # ✅ Add ForeignKey
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    resume_id = Column(Integer, ForeignKey("resumes.id"), nullable=False)
    match_score = Column(Float, nullable=False)  
    matched_skills = Column(Text, nullable=True) # ✅ Add matched_skills : text
    missing_skills = Column(Text, nullable=True) # ✅ Add missing_skills : text
    ats_score_before = Column(Float, nullable=True)  # ✅ Ensure ATS Score fields exist
    ats_score_after = Column(Float, nullable=True)   # ✅ Ensure ATS Score fields exist
    
    #The lambda function is called each time a new row is inserted, ensuring that each row gets the current date and time at the moment of insertion. 
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    calculated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=True)
    
    # Define the relationship between the JobMatch and User models:
    user = relationship("User", back_populates="job_matches")  # ✅ Track job matches per user
    job = relationship("Job", back_populates="job_matches")  # ✅ Link job matches to jobs
    resume = relationship("Resume", back_populates="job_matches")  # ✅ Track resume used in match

    

