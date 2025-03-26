from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.connection import SessionLocal
from app.models.resume import Resume
from app.services.ats_scoring import calculate_ats_score  # ✅ Use service helper
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

    before_score, after_score = calculate_ats_score(resume.parsed_text)  # ✅ Move logic to services
    
    # ✅ Update ATS scores inside `resumes` table
    resume.ats_score_before = before_score
    resume.ats_score_after = after_score
    db.commit()  # ✅ Save changes

    return {
        "resume_id": resume.id,
        "ats_score_before": before_score,
        "ats_score_after": after_score,
        "message": "ATS Score stored successfully."
    }
