# Job Match Score Calculation
from fastapi import APIRouter

router = APIRouter(prefix="/match", tags=["Matching"])

@router.post("/")
def match_resume_to_job(resume_id: int, job_id: int):
    return {"match_score": 85.5, "message": "Matching completed"}
