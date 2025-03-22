from fastapi import APIRouter, Depends, Body
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session
from app.database.connection import SessionLocal
import re
from app.models.job import Job

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class JDInput(BaseModel):
    job_text: str

@router.post("/analyze-jd", tags=["Job Analysis"])
def analyze_jd(payload: JDInput, db: Session = Depends(get_db)):
    jd = payload.job_text.lower()

    # 🔍 Simple keyword-based extraction (can enhance later with NLP)
    skills = re.findall(r"\b(python|fastapi|sql|aws|docker|react|node|postgresql|git)\b", jd)

    return {
        "keywords_found": list(set(skills)),
        "keyword_count": len(set(skills)),
    }


@router.get("/jobs", tags=["Jobs"])
def get_jobs(db: Session = Depends(get_db)):
    jobs = db.query(Job).all()
    return [
        {
            "id": job.id,
            "job_title": job.job_title,
            "company_name": job.company_name,
            "location": job.location,
            "job_url": job.job_url,
            "posted_date": job.posted_date,
        }
        for job in jobs
    ]
