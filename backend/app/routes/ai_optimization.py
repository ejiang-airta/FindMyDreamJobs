# ✅ File: app/routes/ai_optimization.py
# This file contains route-related utilities for AI optimization in the backend.
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from app.database.connection import SessionLocal, get_db
from app.models.resume import Resume
from app.models.match import JobMatch
from app.models.job import Job
from app.services.resume_optimizer import optimize_resume_with_skills_service
from app.services.score_calc import calculate_scores
from app.utils.job_extraction import extract_skills_with_frequency
from typing import List
import logging
from pydantic import BaseModel
from app.config.skills_config import MIN_SKILL_FREQUENCY

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
def optimize_resume(payload: dict = Body(...), db: Session = Depends(get_db)):
    resume_id = payload.get("resume_id")
    job_id = payload.get("job_id")
    justification = payload.get("justification", "")

    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    job = db.query(Job).filter(Job.id == job_id).first()

    if not resume or not job:
        raise HTTPException(status_code=404, detail="Resume or Job not found")

    resume_text = resume.parsed_text
    job_text = job.job_description

    # ✅ Extract keywords from JD
    jd_keywords = extract_skills_with_frequency(job_text)
    resume_keywords = set(resume_text.lower().split())
    # Extract the list of skill names from jd_keywords
    skill_list = [skill_entry["skill"] for skill_entry in jd_keywords["skills"]]

    # ✅ Matched skills = those present in both resume and JD
    matched_skills = [skill for skill in jd_keywords if skill.lower() in resume_keywords]

    # ✅ Emphasized = matched skills with high frequency in JD
    emphasized_skills = []
    for skill in matched_skills:
        if skill in jd_keywords:
            freq = jd_keywords[skill]
            if isinstance(freq, int) and freq >= MIN_SKILL_FREQUENCY:
                emphasized_skills.append(skill)

    missing_skills = [skill for skill in jd_keywords if skill.lower() not in resume_keywords]

    optimized_text, changes_summary = optimize_resume_with_skills_service(
        resume_text,
        matched_skills,
        missing_skills,       # ✅ added this
        emphasized_skills,
        justification
    )


    # 🔍 Calculate ATS score & match score using updated optimized text
    ats_score_final,  match_score_final, _ = calculate_scores(optimized_text, job_text, skill_list)

    # 🔄 Save or update match record
    existing_match = db.query(JobMatch).filter_by(resume_id=resume_id, job_id=job_id).first()
    if existing_match:
        existing_match.match_score_final = match_score_final
        existing_match.ats_score_final = ats_score_final
        existing_match.matched_skills = ",".join(matched_skills)
        existing_match.missing_skills = ",".join(missing_skills)
        existing_match.updated_at = datetime.now(timezone.utc)
    else:
        new_match = JobMatch(
            resume_id=resume_id,
            job_id=job_id,
            match_score_initial=match_score_final,
            ats_score_final=ats_score_final,            # since ats_score_initial only calculated at Upload, so here should be ats_score_final
            matched_skills=",".join(matched_skills),
            missing_skills=",".join(missing_skills),
            created_at=datetime.now(timezone.utc)
        )
        db.add(new_match)

    # 💾 Save optimized resume
    resume.optimized_text = optimized_text
    resume.ats_score_final = ats_score_final
    resume.optimized_at = datetime.now(timezone.utc)

    db.commit()

    # 📜 Logging
    logger.info(f"Resume optimization complete: resume_id={resume.id}, job_id={job.id}")
    logger.info(f"Match Score (Final): {match_score_final}")
    logger.info(f"ATS Score (Final): {ats_score_final}")
    logger.info(f"Emphasized Skills: {emphasized_skills}")
    logger.info(f"Justification: {justification}")
    logger.info(f"Changes Summary: {changes_summary}")

    return {
        "resume_id": resume.id,
        "optimized_text": optimized_text,
        "ats_score_final": ats_score_final,
        "match_score_final": match_score_final,
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
    return {"message": "Resume approved and updated successfully."}
