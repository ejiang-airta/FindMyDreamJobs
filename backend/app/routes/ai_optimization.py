# ✅ File: app/routes/ai_optimization.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.connection import SessionLocal
from app.models.resume import Resume
from app.models.match import JobMatch
from app.models.job import Job
from app.services.resume_optimizer import optimize_resume_with_skills_service
from app.services.ats_scoring import calculate_ats_score
from datetime import datetime, timezone
from typing import List
import logging
from pydantic import BaseModel

# Setup the logger
logger = logging.getLogger("app")

router = APIRouter()

# Database Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ✅ Request Model for `/optimize-resume`
class OptimizationRequest(BaseModel):
    resume_id: int
    job_id: int
    emphasized_skills: List[str]
    justification: str

# 🔹 API: Optimize Resume & Update Final ATS & Match Score

@router.post("/optimize-resume", tags=["Resume Optimization"])
def optimize_resume(
    payload: OptimizationRequest,
    db: Session = Depends(get_db)
):
    resume = db.query(Resume).filter(Resume.id == payload.resume_id).first()
    job = db.query(Job).filter(Job.id == payload.job_id).first()
    match = db.query(JobMatch).filter(
        JobMatch.resume_id == payload.resume_id,
        JobMatch.job_id == payload.job_id
    ).first()

    if not resume or not job:
        raise HTTPException(status_code=404, detail="Resume or Job not found.")

    #  Generate optimized resume using emphasized skills + justification
    optimized_text = optimize_resume_with_skills_service(
        resume_text=resume.parsed_text,
        job_description=job.job_description,
        emphasized_skills=payload.emphasized_skills,
        justification=payload.justification
    )
    # ✅ Recalculate ATS score from optimized text
    _, ats_final = calculate_ats_score(optimized_text)

    # ✅ Recalculate match score final
    jd_keywords = set(job.extracted_skills.lower().split(",")) if job.extracted_skills else set()
    matched = [kw for kw in jd_keywords if kw in optimized_text.lower()]
    match_score_final = round((len(matched) / max(len(jd_keywords), 1)) * 100, 2)

    # 🔄 Update Resume table

    resume.optimized_text = optimized_text
    resume.ats_score_final = ats_final
    resume.is_ai_generated = True
    resume.is_user_approved = False
    resume.updated_at = datetime.now(timezone.utc)

    # 🔄 Update JobMatch table if exists
    if match:
        match.match_score_final = match_score_final
        match.ats_score_final = ats_final
        match.calculated_at = datetime.now(timezone.utc)
    db.commit()
    # logging the optimization process:
    logger.info(f"Starting resume optimization: resume_id={payload.resume_id}, job_id={payload.job_id}")
    logger.debug(f"Optimized resume text: {optimized_text}")
    logger.info(f"Resume optimization completed: resume_id={payload.resume_id}, job_id={payload.job_id}")
    logger.info(f"ATS Score (Final): {ats_final}")
    logger.info(f"Match Score (Final): {match_score_final}")
    logger.info(f"Emphasized Skills: {payload.emphasized_skills}")
    logger.info(f"Justification: {payload.justification}")

    return {
        "resume_id": resume.id,
        "optimized_text": optimized_text,
        "ats_score_final": ats_final,
        "match_score_final": match_score_final,
        "message": "✅ Resume optimized and scores updated successfully!"
    }
    
# 🔹 API: Approve Final Resume
class ResumeApprovalRequest(BaseModel):
    resume_id: int

@router.post("/approve-resume", tags=["Resume Optimization"])
def approve_resume(payload: ResumeApprovalRequest, db: Session = Depends(get_db)):
    resume = db.query(Resume).filter(Resume.id == payload.resume_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    resume.is_user_approved = True
    db.commit()

    return {"message": "✅ Resume marked as approved!"}