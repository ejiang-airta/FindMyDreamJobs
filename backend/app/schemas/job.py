# File: backend/app/schemas/job.py
# This file defines the Pydantic models for job-related data.
from pydantic import BaseModel
from typing import Optional

class JobInput(BaseModel):
    job_link: str | None = None
    job_description: str | None = None
    user_id: int  # Required to track which user added this job

class JobOut(BaseModel):
    id: int
    job_title: str
    company_name: str

    class Config:
        from_attributes = True

class JobIn(BaseModel):
    job_id: str
    job_title: str
    employer_name: str
    employer_logo: Optional[str] = None
    employer_website: Optional[str] = None
    job_location: Optional[str] = None
    job_is_remote: Optional[bool] = False
    job_employment_type: Optional[str] = None
    job_salary: Optional[str] = None
    job_description: Optional[str] = None
    job_google_link: str
    job_posted_at_datetime_utc: str  # ISO string

class SaveJobIn(BaseModel):
    user_id: int
    job: JobIn

class UnsaveJobIn(BaseModel):
    user_id: int
    search_id: str


