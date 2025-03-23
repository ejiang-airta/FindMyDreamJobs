from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.connection import SessionLocal
from app.models.resume import Resume
from app.models.job import Job
from app.models.match import JobMatch
from datetime import datetime
import re
from app.ai.ats_scoring import calculate_ats_score

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# The calculate_ats_score function based on resume_text and returns: before_score and after_score.
@router.post("/ats-score", tags=["ATS Optimization"]) 
def ats_score(resume_id: int, db: Session = Depends(get_db)):
    resume = db.query(Resume).filter(Resume.id == resume_id).first()

    if not resume:
        return {"error": "Resume not found."}

    before_score, after_score = calculate_ats_score(resume.parsed_text)

    return {
        "resume_id": resume.id,
        "ats_score_before": before_score,
        "ats_score_after": after_score,
        "message": "This is a simulated ATS score from ai/ats_scoring.py"
    }        

@router.post("/match-score", tags=["Job Matches"])
def calculate_match(resume_id: int, job_id: int, db: Session = Depends(get_db)):
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    job = db.query(Job).filter(Job.id == job_id).first()

    if not resume or not job:
        return {"error": "Resume or Job not found."}

    resume_text = resume.parsed_text.lower()
    jd_text = job.job_description.lower()

    # Extract keywords from JD
    jd_keywords = re.findall(r"\b(python|fastapi|sql|aws|docker|react|node|postgre|git)\b", jd_text)
    jd_keywords_set = set(jd_keywords)

    # Count matches in resume
    resume_matches = [kw for kw in jd_keywords_set if kw in resume_text]
    score = round((len(resume_matches) / len(jd_keywords_set)) * 100, 2) if jd_keywords_set else 0

    # Optional: save match record
    match = JobMatch(
        user_id=resume.user_id,
        job_id=job.id,
        resume_id=resume.id,
        match_score=score,
        created_at=datetime.now()
    )
    db.add(match)
    db.commit()
    db.refresh(match)

    return {
        "resume_id": resume.id,
        "job_id": job.id,
        "match_score": score,
        "keywords_matched": resume_matches,
        "match_id": match.id
    }

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
