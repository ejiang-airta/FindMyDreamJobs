from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Text, DateTime
from app.database.connection import Base
from datetime import datetime, timezone

class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    file_path = Column(String)
    parsed_text = Column(String)
    optimized_text = Column(Text, nullable=True)
    is_ai_generated = Column(Boolean, default=False)
    is_user_approved = Column(Boolean, default=False)
    #The lambda function is called each time a new row is inserted, ensuring that each row gets the current date and time at the moment of insertion. 
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
