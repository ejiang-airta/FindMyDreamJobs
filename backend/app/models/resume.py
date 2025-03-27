from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Text, DateTime, Float
from sqlalchemy.orm import relationship
from app.database.connection import Base
from datetime import datetime, timezone

class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    file_path = Column(String)  # Path to the uploaded resume file
    parsed_text = Column(Text)  # Extracted raw text from the resume file, original resume
    optimized_text = Column(Text, nullable=True)  # AI-enhanced resume
    is_ai_generated = Column(Boolean, default=False)
    is_user_approved = Column(Boolean, default=False)   
    ats_score_initial = Column(Float, nullable=True)  # ✅ New ATS Score Before
    ats_score_final = Column(Float, nullable=True)   # ✅ New ATS Score After


    #The lambda function is called each time a new row is inserted, ensuring that each row gets the current date and time at the moment of insertion. 
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=True)

    # Define the relationship between the Resume and User models
    user = relationship("User", back_populates="resumes")
    applications = relationship("Application", back_populates="resume")
    job_matches = relationship("JobMatch", back_populates="resume")

