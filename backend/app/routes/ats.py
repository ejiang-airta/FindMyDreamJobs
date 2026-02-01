from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.connection import SessionLocal
from app.models.resume import Resume
from app.models.match import JobMatch
from app.services.score_calc import calculate_scores  # ✅ Use service helper
from datetime import datetime, timezone


router = APIRouter()

# Database Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 🔹 API: Calculate & Store ATS Score
@router.post("/ats-score", tags=["ATS Optimization"])
def ats_score(resume_id: int, db: Session = Depends(get_db)):
    resume = db.query(Resume).filter(Resume.id == resume_id).first()

    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found.")

    ats_score, match_score, warnings = calculate_scores(resume.parsed_text)

    # ✅ Store initial ATS score in job_matches
    job_match = db.query(JobMatch).filter(JobMatch.resume_id == resume.id).first()
    if job_match:
        job_match.ats_score_initial = ats_score
        db.commit()

    # ✅ Update ATS scores inside `resumes` table
    resume.ats_score_initial = ats_score
    resume.ats_score_final = ats_score  # Final score updates after optimization
    db.commit()

    return {
        "resume_id": resume.id,
        "ats_score_initial": ats_score,
        "ats_score_final": ats_score,
        "warnings": warnings,
        "message": "ATS Score stored successfully."
    }
