from sqlalchemy import Column, Integer, String, DateTime
from app.database.connection import Base

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    job_title = Column(String, nullable=False)
    company_name = Column(String)
    location = Column(String)
    job_description = Column(String)
    job_url = Column(String)
    posted_date = Column(DateTime)
