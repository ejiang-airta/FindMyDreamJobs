from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from app.database.connection import Base
from datetime import datetime, timezone

class JobMatch(Base):
    __tablename__ = "job_matches"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    resume_id = Column(Integer)
    job_id = Column(Integer)
    match_score = Column(Integer)
    ats_score_before = Column(Integer, nullable=True)
    ats_score_after = Column(Integer, nullable=True)
    
    #The lambda function is called each time a new row is inserted, ensuring that each row gets the current date and time at the moment of insertion. 
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
