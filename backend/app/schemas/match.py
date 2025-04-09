from pydantic import BaseModel
from datetime import datetime

class MatchTrendOut(BaseModel):
    job_id: int
    job_title: str
    company_name: str
    match_score_initial: float | None = None
    match_score_final: float | None = None
    created_at: datetime
