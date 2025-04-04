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
from app.utils.job_extraction import extract_skills_with_frequency
from app.config.skills_config import SKILL_KEYWORDS

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

    jd_skill_freq = extract_skills_with_frequency(jd_text, SKILL_KEYWORDS)
    resume_skill_freq = extract_skills_with_frequency(resume_text, SKILL_KEYWORDS)

    jd_skills = set(jd_skill_freq.keys())
    resume_skills = set(resume_skill_freq.keys())

    matched = list(jd_skills & resume_skills)
    missing = list(jd_skills - resume_skills)

    match = db.query(JobMatch).filter(
        JobMatch.resume_id == resume.id, JobMatch.job_id == job.id
    ).first()

    # 🆕 Calculate match scores:
    match_score=round(len(matched) / max(len(jd_skills), 1) * 100, 2),
    ats_score=round(len(matched) / max(len(resume_skills), 1) * 100, 2),
    # ✅ Save match record 
    if match is None:
        # 🆕 New match
        match = JobMatch(
            user_id=resume.user_id,
            job_id=job.id,
            resume_id=resume.id,
            match_score_initial=match_score,
            ats_score_initial=ats_score,
            matched_skills=",".join(matched),
            missing_skills=",".join(missing),
            created_at=datetime.now(timezone.utc),
        )
    else:
        # 🔁 Existing match: update final scores
        match.match_score_final = match_score
        match.ats_score_final = ats_score
        match.calculated_at = datetime.now(timezone.utc)
        match.matched_skills = ",".join(matched)
        match.missing_skills = ",".join(missing)
    db.add(match)
    db.commit()
    db.refresh(match)

    return {
        "resume_id": resume.id,
        "job_id": job.id,
        "match_score": match.match_score_final or match.match_score_initial,
        "ats_score": match.ats_score_final or match.ats_score_initial,
        "matched_skills": matched,
        "missing_skills": missing
    }

# 🔹 API: Get All Matches for all users - only for admin to use:
@router.get("/matches", tags=["Job Matches"])
def get_matches(db: Session = Depends(get_db)):
    matches = db.query(JobMatch).all()
    return [
        {
            "id": match.id,
            "user_id": match.user_id,
            "job_id": match.job_id,
            "resume_id": match.resume_id,
            "match_score_initial": match.match_score_initial,
            "match_score_final": match.match_score_final,
            "created_at": match.created_at,
        }
        for match in matches
    ]

# ✅ API: Get All Matches for a User
@router.get("/matches/{user_id}", tags=["Job Matches"])
def get_user_matches(user_id: int, db: Session = Depends(get_db)):
    matches = (
        db.query(JobMatch)
        .filter(JobMatch.user_id == user_id)
        .join(Job)
        .join(Resume)
        .with_entities(
            JobMatch.id.label("match_id"),
            JobMatch.job_id,
            Job.job_title,
            Job.company_name,
            JobMatch.resume_id,
            JobMatch.match_score_initial,
            JobMatch.match_score_final,
            JobMatch.ats_score_initial,
            JobMatch.ats_score_final,
            JobMatch.created_at
        )
        .order_by(JobMatch.created_at.desc())
        .all()
    )

    return [dict(m._mapping) for m in matches]