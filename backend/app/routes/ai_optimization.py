from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.connection import SessionLocal
from app.models.resume import Resume
from app.models.match import JobMatch
from app.services.resume_optimizer import optimize_resume
from datetime import datetime, timezone

router = APIRouter()

# Database Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 🔹 API: Optimize Resume & Update Final ATS & Match Score
@router.post("/optimize-resume", tags=["AI Optimization"])
def optimize_resume(resume_id: int, job_id: int, db: Session = Depends(get_db)):

    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    job_match = db.query(JobMatch).filter(
        JobMatch.resume_id == resume_id, JobMatch.job_id == job_id
    ).first()

    if not resume or not job_match:
        raise HTTPException(status_code=404, detail="Resume or Job Match not found.")

    # ✅ AI Enhancement
    optimized_text = optimize_resume(resume.parsed_text, job_match.missing_skills)

    # ✅ Update Resume
    resume.optimized_text = optimized_text
    resume.is_ai_generated = True
    resume.ats_score_final = job_match.ats_score_final    # Sync scores
    db.commit()

    return {
        "resume_id": resume.id,
        "optimized": True,
        "message": "Resume optimized successfully."
    }
