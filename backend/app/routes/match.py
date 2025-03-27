from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.connection import SessionLocal
from app.models.resume import Resume
from app.models.job import Job
from app.models.match import JobMatch
from datetime import datetime, timezone
import re
from pydantic import BaseModel
import random

router = APIRouter()

# Database Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ Request Model for `/match-score`
class MatchRequest(BaseModel):
    resume_id: int
    job_id: int

# 🔹 API: Calculate Resume-JD Match Score
@router.post("/match-score", tags=["Job Matches"])
def calculate_match(request: MatchRequest, db: Session = Depends(get_db)):
    resume = db.query(Resume).filter(Resume.id == request.resume_id).first()
    job = db.query(Job).filter(Job.id == request.job_id).first()

    if not resume or not job:
        raise HTTPException(status_code=404, detail="Resume or Job not found.")

    resume_text = resume.parsed_text.lower()
    jd_text = job.job_description.lower()

    # Extract keywords from JD
    jd_keywords = set(re.findall(r"\b(python|fastapi|sql|aws|docker|react|node|postgre|git)\b", jd_text))
    jd_keywords_set = set(jd_keywords)
    print("🔍 Extracted JD Keywords:", jd_keywords_set)  # 👈 Debugging Print


    # Count matches in resume
    resume_matches = [kw for kw in jd_keywords_set if kw in resume_text]
    missing_skills = list(jd_keywords_set - set(resume_matches))
    print("✅ Matched Resume Keywords:", resume_matches)  # 👈 Debugging Print

    score = round((len(resume_matches) / max(len(jd_keywords), 1)) * 100, 2)  # Avoid zero division

    # ✅ Save match record 
    match = JobMatch(
        user_id=resume.user_id,
        job_id=job.id,
        resume_id=resume.id,
        match_score_initial=score,  # ✅ Updated field name
        matched_skills=",".join(resume_matches),  # ✅ Store matched skills
        missing_skills=",".join(missing_skills),  # ✅ Store missing skills
        created_at=datetime.now(timezone.utc),  # ✅ Use timezone-aware datetime
        calculated_at=datetime.now(timezone.utc)  # ✅ Ensure timestamp is stored
    )

    db.add(match)
    db.commit()
    db.refresh(match)

    return {
        "resume_id": resume.id,
        "job_id": job.id,
        "match_score_initial": score,
        "keywords_matched": resume_matches,
        "missing_skills": missing_skills,
        "match_id": match.id
    }


# 🔹 API: Get All Matches
@router.get("/matches", tags=["Job Matches"])
def get_matches(db: Session = Depends(get_db)):
    matches = db.query(JobMatch).all()
    return [
        {
            "id": match.id,
            "user_id": match.user_id,
            "job_id": match.job_id,
            "resume_id": match.resume_id,
            "match_score": match.match_score,
            "created_at": match.created_at,
        }
        for match in matches
    ]
