# File: app/routes/match.py
# This file contains route-related utilities for job matching in the backend.
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.connection import SessionLocal
from app.models.resume import Resume
from app.models.job import Job
from app.models.match import JobMatch
from datetime import datetime, timezone
from pydantic import BaseModel
from app.utils.job_extraction import extract_skills_with_frequency
from app.config.skills_config import SKILL_KEYWORDS
from app.services.ats_scoring import calculate_ats_score

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

    # ✅ Extract structured skills from job.extracted_skills JSONB
    extracted = job.extracted_skills or {}
    jd_keywords = set()
    skill_map = {}

    if isinstance(extracted, dict):
        jd_skill_objs = extracted.get("skills", [])
        skill_map = {item["skill"].lower(): item["skill"] for item in jd_skill_objs if "skill" in item}
        jd_keywords = set(skill_map.keys())

    # ✅ Match vs resume
    matched_skills = [skill_map[kw] for kw in jd_keywords if kw in resume_text]
    missing_skills = [skill_map[kw] for kw in jd_keywords if kw not in resume_text]

    # ✅ Compute scores
    match_score = round((len(matched_skills) / max(len(jd_keywords), 1)) * 100, 2)
    ats_score_before, ats_score_after, _ = calculate_ats_score(resume_text)

    # ✅ Find or create JobMatch
    match = db.query(JobMatch).filter(
        JobMatch.resume_id == resume.id, JobMatch.job_id == job.id
    ).first()

    if match is None:
        # 🆕 First time → insert with initial scores
        match = JobMatch(
            user_id=resume.user_id,
            job_id=job.id,
            resume_id=resume.id,
            match_score_initial=match_score,
            ats_score_initial=ats_score_before,
            matched_skills=",".join(matched_skills),
            missing_skills=",".join(missing_skills),
            created_at=datetime.now(timezone.utc),
        )
        db.add(match)
    else:
        # 🔁 Existing → update final scores only
        match.match_score_final = match_score
        match.ats_score_final = ats_score_after
        match.calculated_at = datetime.now(timezone.utc)
        match.matched_skills = ",".join(matched_skills)
        match.missing_skills = ",".join(missing_skills)

    db.commit()
    db.refresh(match)

    return {
        "resume_id": resume.id,
        "job_id": job.id,
        "match_score": match.match_score_final or match.match_score_initial,
        "ats_score": match.ats_score_final or match.ats_score_initial,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills
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
