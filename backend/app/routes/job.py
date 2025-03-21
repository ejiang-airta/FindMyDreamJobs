# Job Description Analysis
from fastapi import APIRouter

router = APIRouter(prefix="/job", tags=["Job"])

@router.post("/analyze")
def analyze_job(job_text: str):
    return {"job_id": 201, "message": "Job analyzed successfully"}
