from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timezone
from app.database.connection import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Define the relationship between the User and Resume models
    resumes = relationship("Resume", back_populates="user")  # ✅ Track resumes uploaded by user
    applications = relationship("Application", back_populates="user")  # ✅ Track jobs applied for by user
    job_matches = relationship("JobMatch", back_populates="user")  # ✅ Track past match results per user
