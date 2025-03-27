from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.connection import SessionLocal
from app.models.application import Application
from datetime import datetime, timezone

router = APIRouter()

# Database Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 🔹 API: Submit Job Application
@router.post("/submit-application", tags=["Applications"])
def submit_application(user_id: int, job_id: int, resume_id: int, application_url: str, db: Session = Depends(get_db)):
    application = Application(
        user_id=user_id,
        job_id=job_id,
        resume_id=resume_id,
        application_url=application_url,
        application_status="Submitted",
        applied_date=datetime.now(timezone.utc)
    )

    db.add(application)
    db.commit()

    return {"message": "Application submitted successfully", "application_id": application.id}

# 🔹 API: Update Application Status
@router.put("/update-application-status", tags=["Applications"])
def update_application_status(application_id: int, status: str, db: Session = Depends(get_db)):
    application = db.query(Application).filter(Application.id == application_id).first()

    if not application:
        raise HTTPException(status_code=404, detail="Application not found.")

    application.application_status = status
    db.commit()

    return {"message": "Application status updated successfully"}

# application tracking
@router.post("/log")
def log_application(job_id: int, user_id: int):
    return {"application_id": 301, "message": "Application logged"}
