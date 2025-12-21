# ✅ File: //backend/app/routes/job.py
import requests
from bs4 import BeautifulSoup
from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.models.job import Job
from app.models.saved_job import SavedJob
from datetime import datetime, timezone
import spacy
from app.schemas.job import JobInput, JobOut, JobIn, SaveJobIn, UnsaveJobIn  # centeralized JobInput and JobOut to schemas/job.py
from app.utils.salary_extractor import extract_salary  # Import salary extraction utility
from app.utils.job_extraction import (
    extract_title,
    extract_company_name,
    extract_skills_with_frequency,
    extract_experience,
    extract_location,
)

router = APIRouter()

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

from pydantic import BaseModel
from typing import Optional

class JobUpdateIn(BaseModel):
    job_title: Optional[str] = None
    company_name: Optional[str] = None
    location: Optional[str] = None
    salary: Optional[str] = None
    applicants_count: Optional[str] = None

@router.put("/jobs/{job_id}", tags=["Jobs"])
def update_job(job_id: int, payload: JobUpdateIn, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    # Update only provided fields
    for field, value in payload.dict(exclude_unset=True).items():
        setattr(job, field, value)

    db.commit()
    db.refresh(job)
    return job


@router.post("/parse-job-description", tags=["Jobs"])
async def parse_job_description(job: JobInput, db: Session = Depends(get_db)):
    if not job.job_link and not job.job_description:
        raise HTTPException(status_code=400, detail="Job link or description is required.")

    # 🔍 Use raw text if provided, else fetch from job link (scraper can be added later)
    # If no job description is provided but a job_link is, try to fetch content
    description = job.job_description
    if not description and job.job_link:
        try:
            response = requests.get(job.job_link, timeout=5)
            soup = BeautifulSoup(response.text, "html.parser")
            # Simple strategy: Get largest <p> or all text content
            paragraphs = soup.find_all("p")
            description = max(paragraphs, key=lambda p: len(p.text)).text if paragraphs else soup.get_text()
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to extract job description from link: {str(e)}")

    if not description:
        raise HTTPException(status_code=400, detail="Job description could not be extracted.")


    # 🧠 mostly using spaCy to extract:
    skills = extract_skills_with_frequency(description)
    title = extract_title(description)
    experience = extract_experience(description)
    location = extract_location(description)
    company = extract_company_name(description)
    salary = extract_salary(description) # Extract salary if available, else None

    # 🧾 Save to DB
    new_job = Job(
        user_id=job.user_id,
        job_link=job.job_link or "N/A",
        job_description=description,
        job_title=title,
        extracted_skills = skills,
        required_experience=experience,
        company_name=company or "Unknown Company",  # ✅ Fallback if extract company return nothing
        location=location,
        salary=salary,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    return {
        "message": "✅ Job parsed and saved.",
        "job_id": new_job.id,
        "company": company,
        "title": title,
        "skills": skills,
        "experience": experience,
        "company_name": company,
        "location": location,
        "salary": salary,
    }

@router.post("/analyze-searched-job", tags=["Jobs"])
async def analyze_searched_job(request: Request, db: Session = Depends(get_db)):
    """
    This route is used for jobs returned by the search results with structured data.
    """
    payload = await request.json()
    required_fields = ["job_title", "employer_name", "job_description", "user_id"]
    for field in required_fields:
        if field not in payload:
            raise HTTPException(status_code=400, detail=f"Missing required field: {field}")

    job_title = payload["job_title"]
    employer_name = payload["employer_name"]
    job_description = payload["job_description"]
    job_location = payload.get("job_location") or extract_location(job_description)
    user_id = payload["user_id"]
    job_link = payload.get("job_link")
    salary = payload.get("salary") or extract_salary(job_description)

    extracted_skills: dict[str, list[str]] = extract_skills_with_frequency(job_description)

    new_job = Job(
        job_title=job_title,
        company_name=employer_name,
        job_description=job_description,
        location=job_location,
        user_id=user_id,
        job_link=job_link,
        salary=salary,
        extracted_skills=extracted_skills,
        created_at=datetime.now(timezone.utc),
    )
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return new_job

# Get all jobs by user:
@router.get("/jobs/by-user/{user_id}", tags=["Jobs"])
def get_jobs_by_user(user_id: int, db: Session = Depends(get_db)):
    jobs = db.query(Job).filter(Job.user_id == user_id).all()

    if not jobs:
        raise HTTPException(status_code=404, detail="No job found for this user.")

    return jobs

# ✅ Get jobs by job_id
@router.get("/jobs/{job_id}", tags=["Jobs"])
def get_job_by_id(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    # Return emphasized skills if they exist
    extracted = job.extracted_skills or {}
    emphasized_skills = extracted.get("emphasized_skills", [])

    return {
        "job_id": job.id,
        "job_title": job.job_title,
        "company_name": job.company_name,
        "emphasized_skills": emphasized_skills,
    }

# get all saved jobs for a user:
@router.post("/save-job", tags=["Jobs"])
def save_job(payload: SaveJobIn, db: Session = Depends(get_db)):
    print("🔍 Incoming save-job payload:", payload)

    user_id = payload.user_id
    job_data = payload.job

    # Prevent duplicate saves
    existing = db.query(SavedJob).filter_by(user_id=user_id, search_id=job_data.job_id).first()
    if existing:
        return {"message": "Job already saved."}
    
    try:
        parsed_posted_at = datetime.fromisoformat(job_data.job_posted_at_datetime_utc)
    except Exception:
        parsed_posted_at = None  # or fallback to datetime.utcnow(), up to your preference

    new_saved = SavedJob(
        user_id=user_id,
        search_id=job_data.job_id,
        job_title=job_data.job_title,
        employer_name=job_data.employer_name,
        employer_logo=job_data.employer_logo,
        employer_website=job_data.employer_website,
        job_location=job_data.job_location,
        job_is_remote=job_data.job_is_remote,
        job_employment_type=job_data.job_employment_type,
        job_salary=job_data.job_salary,
        job_description=job_data.job_description,
        job_apply_link=job_data.job_google_link,
        job_posted_at=parsed_posted_at,
    )

    db.add(new_saved)
    db.commit()
    db.refresh(new_saved)

    return {"message": "Job saved successfully."}

# remove the saved job for a user:
@router.post("/unsave-job", tags=["Jobs"])
def unsave_job(payload: UnsaveJobIn, db: Session = Depends(get_db)):
    user_id = payload.user_id
    search_id = payload.search_id

    existing = db.query(SavedJob).filter_by(user_id=user_id, search_id=search_id).first()
    if not existing:
        raise HTTPException(status_code=404, detail="Saved job not found.")

    db.delete(existing)
    db.commit()
    return {"message": "Job unsaved successfully."}

@router.get("/saved-jobs/{user_id}", tags=["Jobs"])
async def get_saved_jobs(user_id: int, db: Session = Depends(get_db)):
    saved = db.query(SavedJob).filter(SavedJob.user_id == user_id).all()

    # Return full job data for frontend display
    return [
        {
            "search_id": s.search_id,
            "job_id": s.search_id,  # for compatibility with frontend job_id checks
            "job_title": s.job_title,
            "employer_name": s.employer_name,
            "employer_logo": s.employer_logo,
            "employer_website": s.employer_website,
            "job_location": s.job_location,
            "job_is_remote": s.job_is_remote,
            "job_employment_type": s.job_employment_type,
            "job_salary": s.job_salary or extract_salary(s.job_description or ""),
            "job_google_link": s.job_apply_link,
            "job_description": s.job_description,
            "job_posted_at_datetime_utc": (s.job_posted_at.isoformat() if s.job_posted_at else datetime.utcnow().isoformat()),
        }
        for s in saved
    ]
