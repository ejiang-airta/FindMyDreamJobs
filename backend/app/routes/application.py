from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.connection import SessionLocal
from app.models.application import Application

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/applications", tags=["Applications"])
def get_applications(db: Session = Depends(get_db)):
    apps = db.query(Application).all()
    return [
        {
            "id": app.id,
            "user_id": app.user_id,
            "job_id": app.job_id,
            "resume_id": app.resume_id,
            "application_url": app.application_url,
            "application_status": app.application_status,
            "applied_date": app.applied_date,
        }
        for app in apps
    ]
# application tracking
@router.post("/log")
def log_application(job_id: int, user_id: int):
    return {"application_id": 301, "message": "Application logged"}
