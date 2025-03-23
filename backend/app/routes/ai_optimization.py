from fastapi import APIRouter, UploadFile, File, Depends, Form
from sqlalchemy.orm import Session
from app.database.connection import SessionLocal
from app.models.resume import Resume
from datetime import datetime
import os
import uuid
from app.config.settings import UPLOAD_DIR

router = APIRouter()

UPLOAD_DIR = "uploads/resumes"
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/optimize-resume", tags=["AI Resume Optimization"])
def optimize_resume(resume_id: int, db: Session = Depends(get_db)):
    resume = db.query(Resume).filter(Resume.id == resume_id).first()

    if not resume:
        return {"error": "Resume not found."}

    # Very simple "optimized" version (placeholder)
    optimized = resume.parsed_text + "\n\n[Optimized by AI ✅]"

    resume.optimized_text = optimized
    resume.is_ai_generated = True
    db.commit()
    db.refresh(resume)

    return {
        "resume_id": resume.id,
        "optimized_text": optimized,
        "message": "Resume optimized with placeholder AI logic."
    }
