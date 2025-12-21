# ✅ File: app/routes/application.py (append to existing routes if present)
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.connection import SessionLocal
from app.models.application import Application
from app.models.resume import Resume
from app.models.match import JobMatch
from sqlalchemy import func

from app.models.job import Job
from datetime import datetime, timezone
from pydantic import BaseModel

router = APIRouter()

# ✅ Request Model for `/submit-application`
class ApplicationRequest(BaseModel):
    resume_id: int
    job_id: int
    application_url: str

# Database Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 🔹 API: Submit Job Application
@router.post("/submit-application", tags=["Applications"])
def submit_application(req: ApplicationRequest, db: Session = Depends(get_db)):
    resume = db.query(Resume).filter(Resume.id == req.resume_id).first()
    job = db.query(Job).filter(Job.id == req.job_id).first()

    if not resume or not job:
        raise HTTPException(status_code=404, detail="Resume or Job not found.")

    application = Application(
        user_id=resume.user_id,
        job_id=req.job_id,
        resume_id=req.resume_id,
        application_url=req.application_url,
        application_status="Application Submitted",
        applied_date=datetime.now(timezone.utc)
    )

    db.add(application)
    db.commit()
    db.refresh(application)

    return {
        "application_id": application.id,
        "job_id": req.job_id,
        "resume_id": req.resume_id,
        "application_url": req.application_url,
        "status": "✅ Application recorded successfully."
    }

# ✅ API: Update Status
@router.put("/update-application-status", tags=["Applications"])
def update_application_status(application_id: int, status: str, db: Session = Depends(get_db)):
    application = db.query(Application).filter(Application.id == application_id).first()

    if not application:
        raise HTTPException(status_code=404, detail="Application not found.")

    application.application_status = status
    db.commit()

    return {"message": "✅ Application status updated successfully."}

# application tracking
@router.post("/log")
def log_application(job_id: int, user_id: int):
    return {"application_id": 301, "message": "📝 Application logged."}

# 🔹 API: Get All Applications for a User
@router.get("/applications/{user_id}", tags=["Applications"])
def get_user_applications(user_id: int, db: Session = Depends(get_db)):
    apps = (
        db.query(Application)
        .filter(Application.user_id == user_id)
        .join(Job, Application.job_id == Job.id)
        .join(Resume, Application.resume_id == Resume.id)
        .outerjoin(
            JobMatch,
            (JobMatch.job_id == Application.job_id) & (JobMatch.resume_id == Application.resume_id)
        )
        .with_entities(
            Application.id.label("application_id"),
            Application.job_id,
            Job.job_title,
            Job.company_name,
            Job.salary,
            Job.location,
            Job.applicants_count,
            Resume.resume_name,
            Application.resume_id,
            Application.application_status,
            Application.application_url,
            Application.applied_date,

            # ✅ NEW: match score (prefer final, else initial)
            func.coalesce(JobMatch.match_score_final, JobMatch.match_score_initial).label("match_score"),

            # ✅ NEW: ATS score (prefer final, else initial)
            func.coalesce(Resume.ats_score_final, Resume.ats_score_initial).label("ats_score"),
        )
        .order_by(Application.applied_date.desc())
        .all()
    )


    return [dict(app._mapping) for app in apps]

