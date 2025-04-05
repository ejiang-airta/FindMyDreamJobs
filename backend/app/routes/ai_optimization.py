# ✅ File: app/routes/ai_optimization.py
# This file contains route-related utilities for AI optimization in the backend.
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.connection import SessionLocal, get_db
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

    if not resume or not job:
        raise HTTPException(status_code=404, detail="Resume or Job not found.")
    
    # Check if the resume is already optimized
    match = db.query(JobMatch).filter(
        JobMatch.resume_id == payload.resume_id,
        JobMatch.job_id == payload.job_id
    ).first()

    # ✅ Extract skills from job JSONB
    extracted = job.extracted_skills or {}
    jd_skill_objs = extracted.get("skills", [])
    jd_keywords = {item["skill"].lower() for item in jd_skill_objs if "skill" in item}

    # ✅ Match vs resume text
    matched_skills = [kw for kw in jd_keywords if kw in resume.parsed_text.lower()]
    missing_skills = list(jd_keywords - set(matched_skills))

    # ✅ Run GPT-based optimizer service:
    optimized_text, changes_summary = optimize_resume_with_skills_service(
        resume_text=resume.parsed_text,
        matched_skills=matched_skills,
        missing_skills=missing_skills,
        emphasized_skills=payload.emphasized_skills,
        justification=payload.justification
    )
    # ✅ Recalculate ATS score from optimized text
    _, ats_final = calculate_ats_score(optimized_text)
    # ✅ Recalculate match score final
    final_match_score = round((len(matched_skills) / max(len(jd_keywords), 1)) * 100, 2)

    # 🔄 Update Resume table
    resume.optimized_text = optimized_text
    resume.ats_score_final = ats_final
    resume.is_ai_generated = True
    resume.is_user_approved = False
    resume.updated_at = datetime.now(timezone.utc)

    if match:
        # 🔁 Update final values
        match.match_score_final = final_match_score
        match.ats_score_final = ats_final
        match.calculated_at = datetime.now(timezone.utc)
        match.changes_summary = ", ".join(changes_summary)

    else:
        # 🆕 Create new match record with initial scores
        match = JobMatch(
            user_id=resume.user_id,
            job_id=job.id,
            resume_id=resume.id,
            match_score_initial=final_match_score,
            ats_score_initial=ats_final,
            matched_skills=",".join(matched_skills),
            missing_skills=",".join(missing_skills),
            created_at=datetime.now(timezone.utc),
            changes_summary=", ".join(changes_summary)
        )
        db.add(match)

    db.commit()

    # 📜 Logging
    logger.info(f"Resume optimization complete: resume_id={resume.id}, job_id={job.id}")
    logger.info(f"Match Score (Final): {final_match_score}")
    logger.info(f"ATS Score (Final): {ats_final}")
    logger.info(f"Emphasized Skills: {payload.emphasized_skills}")
    logger.info(f"Justification: {payload.justification}")
    logger.info(f"Changes Summary: {changes_summary}")

    return {
        "resume_id": resume.id,
        "optimized_text": optimized_text,
        "ats_score_final": ats_final,
        "match_score_final": final_match_score,
        "changes_summary": changes_summary,
        "message": "✅ Resume optimized and scores updated successfully!"
    }

    
# 🔹 API: Approve Final Resume
class ResumeApprovalRequest(BaseModel):
    resume_id: int

@router.post("/approve-resume", tags=["Resume Optimization"])
def approve_resume(payload: dict, db: Session = Depends(get_db)):
    resume_id = int(payload.get("resume_id"))
    resume = db.query(Resume).filter(Resume.id == resume_id).first()

    if not resume or not resume.optimized_text:
        raise HTTPException(status_code=404, detail="Resume or optimized version not found.")

    # ✅ Overwrite parsed_text with optimized version
    resume.parsed_text = resume.optimized_text
    resume.is_approved = True
    resume.updated_at = datetime.now(timezone.utc)

    db.commit()
    return { "message": "Resume approved and updated successfully." }