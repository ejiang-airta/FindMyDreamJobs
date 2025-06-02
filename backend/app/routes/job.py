# ✅ File: //backend/app/routes/job.py
import requests
from bs4 import BeautifulSoup
from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.models.job import Job
from typing import List
from datetime import datetime, timezone
import re
import spacy
from app.schemas.job import JobOut, JobInput  # centeralized JobInput and JobOut to schemas/job.py
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
        "emphasized_skills": job.extracted_skills.get("emphasized_skills", []) if job.extracted_skills else [],
    }

# get all saved jobs for a user:
@router.post("/toggle-save-job", tags=["Jobs"])
async def toggle_save_job(request: Request, db: Session = Depends(get_db)):
    """
    Toggle save/unsave for a job using a user_id + job_link combo.
    """
    payload = await request.json()
    user_id = payload.get("user_id")
    job_link = payload.get("job_link")

    if not user_id or not job_link:
        raise HTTPException(status_code=400, detail="user_id and job_link are required")

    job = db.query(Job).filter(Job.user_id == user_id, Job.redirect_url == job_link).first()
    if job:
        db.delete(job)
        db.commit()
        return {"message": "Job unsaved", "action": "unsaved"}
    else:
        new_job = Job(
            job_title=payload.get("job_title", "N/A"),
            company_name=payload.get("employer_name", "N/A"),
            job_description=payload.get("job_description", "N/A"),
            location=payload.get("job_location", "N/A"),
            user_id=user_id,
            job_link=job_link,
            salary=payload.get("salary"),
            extracted_skills="{}",
            created_at=datetime.now(timezone.utc),
        )
        db.add(new_job)
        db.commit()
        db.refresh(new_job)
        return {"message": "Job saved", "action": "saved", "job_id": new_job.id}