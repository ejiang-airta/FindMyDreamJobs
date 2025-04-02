# ✅ File: //backend/app/routes/job.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database.connection import get_db
from app.models.job import Job
from datetime import datetime, timezone
import re

router = APIRouter()

class JobInput(BaseModel):
    job_link: str | None = None
    job_description: str | None = None
    user_id: int  # Required to track which user added this job

@router.post("/parse-job-description", tags=["Jobs"])
async def parse_job_description(job: JobInput, db: Session = Depends(get_db)):
    if not job.job_link and not job.job_description:
        raise HTTPException(status_code=400, detail="Job link or description is required.")

    # 🔍 Use raw text if provided, else fetch from job link (scraper can be added later)
    description = job.job_description or "N/A"

    # 🧠 Basic parsing logic — can be replaced with spacy or custom model
    skills = extract_skills(description)
    title = extract_title(description)
    experience = extract_experience(description)
    location = extract_location(description)
    company = extract_company(description)

    # 🧾 Save to DB
    new_job = Job(
        user_id=job.user_id,
        job_link=job.job_link or "N/A",
        job_description=description,
        job_title=title,
        extracted_skills=skills,
        required_experience=experience,
        company_name=company or "Unknown Company",  # ✅ Fallback if extract company return nothing
        location=location,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    return {
        "message": "✅ Job parsed and saved.",
        "job_id": new_job.id,
        "title": title,
        "skills": skills,
        "experience": experience,
        "company_name": company,
        "location": location,
    }
# ------------------------------
# 🧠 Utility extractors
# ------------------------------
# ✅ Basic skill extractor (can be replaced with AI model later)
def extract_skills(text: str):
    keywords = ["Python", "Django", "FastAPI", "React", "SQL", "AWS", "Kubernetes"]
    return [kw for kw in keywords if kw.lower() in text.lower()]

def extract_title(text: str):
    match = re.search(r"(?i)(software engineer|developer|data scientist|backend engineer)", text)
    return match.group(0) if match else "Unknown Title"

def extract_experience(text: str):
    match = re.search(r"\d+\+?\s+years?", text)
    return match.group(0) if match else "Unspecified"

def extract_location(text: str):
    known_locations = ["Vancouver", "Toronto", "Remote", "San Francisco", "New York", "Seattle", "Austin"]
    for loc in known_locations:
        if loc.lower() in text.lower():
            return loc
    return None

def extract_company(text: str):
    match = re.search(r"(?i)(at|@)\s+([A-Z][a-zA-Z0-9&.\- ]+)", text)
    return match.group(2).strip() if match else None
