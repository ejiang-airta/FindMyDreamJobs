# File: backend/app/schemas/job.py
# This file defines the Pydantic models for job-related data.
from pydantic import BaseModel

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