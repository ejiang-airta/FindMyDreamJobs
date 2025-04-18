# ✅ File: //backend/app/routes/job.py
import requests
from bs4 import BeautifulSoup
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.models.job import Job
from typing import List
from datetime import datetime, timezone
import re
import spacy
from app.schemas.job import JobOut, JobInput  # centeralized JobInput and JobOut to schemas/job.py
from app.utils.job_extraction import (
    extract_title,
    extract_company_name,
    extract_skills_with_frequency,
    extract_experience,
    extract_location
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
    }
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