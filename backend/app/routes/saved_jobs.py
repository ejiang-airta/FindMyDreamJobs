# ✅ File: backend/app/routes/saved_jobs.py
from fastapi import APIRouter, HTTPException
from app.schemas.job import SaveJobIn
from app.models.saved_job import SavedJob
from app.database.connection import SessionLocal
from sqlalchemy.exc import IntegrityError
from datetime import datetime

router = APIRouter()

@router.post("/save-job")
def save_job(payload: SaveJobIn):
    db = SessionLocal()
    try:
        job = payload.job
        saved_job = SavedJob(
            user_id=payload.user_id,
            search_id=job.job_id,
            job_title=job.job_title,
            employer_name=job.employer_name,
            employer_logo=job.employer_logo,
            employer_website=job.employer_website,
            job_location=job.job_location,
            job_is_remote=job.job_is_remote,
            job_employment_type=job.job_employment_type,
            job_salary=job.job_salary,
            job_description=job.job_description,
            job_apply_link=job.job_google_link,
            job_posted_at=datetime.fromisoformat(job.job_posted_at_datetime_utc.replace("Z", "+00:00")),
        )
        db.add(saved_job)
        db.commit()
        return {"message": "Job saved"}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Job already saved")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()
