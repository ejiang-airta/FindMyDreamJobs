# Application Tracking)
from fastapi import APIRouter

router = APIRouter(prefix="/application", tags=["Application"])

@router.post("/log")
def log_application(job_id: int, user_id: int):
    return {"application_id": 301, "message": "Application logged"}
