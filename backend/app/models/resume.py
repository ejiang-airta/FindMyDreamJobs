from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from app.database.connection import Base

class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    file_path = Column(String)
    parsed_text = Column(String)
    created_at = Column(DateTime)
