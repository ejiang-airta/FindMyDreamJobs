from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

class JobInput(BaseModel):
    job_link: str = None
    job_description: str = None

@router.post("/parse-job-description", tags=["Jobs"])
async def parse_job_description(job: JobInput):
    if not job.job_link and not job.job_description:
        raise HTTPException(status_code=400, detail="Job link or description is required.")

    # Simulated parsing logic (replace this with actual NLP extraction)
    extracted_data = {
        "title": "Software Engineer",
        "skills": ["Python", "Django", "REST APIs"],
        "experience": "3+ years"
    }

    return extracted_data
