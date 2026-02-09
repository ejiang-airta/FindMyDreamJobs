# File: backend/app/schemas/jdi.py
# Pydantic schemas for JDI candidate feed and actions
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# --- Request schemas ---

class JDIRunRequest(BaseModel):
    """Trigger an ingestion scan."""
    window_hours: int = Field(default=24, ge=1, le=168)


class JDIPromoteRequest(BaseModel):
    """Promote a JDI candidate to a Job record."""
    mode: str = Field(..., pattern="^(save|analyze)$")   # save | analyze


# --- Response schemas ---

class JDICandidateListItem(BaseModel):
    """Summary item for the JDI feed list."""
    id: str
    source: str
    title: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    employment_type: Optional[str] = None
    salary_text: Optional[str] = None
    match_score: Optional[int] = None
    match_reasons: Optional[list[str]] = None
    status: str
    seen_at: Optional[datetime] = None
    job_url_raw: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class JDICandidateDetail(JDICandidateListItem):
    """Full detail view including JD text."""
    jd_text: Optional[str] = None
    jd_extraction_confidence: Optional[int] = None
    job_url_canonical: Optional[str] = None
    selected_resume_id: Optional[int] = None
    updated_at: Optional[datetime] = None


class JDICandidateFeed(BaseModel):
    """Paginated feed response."""
    candidates: list[JDICandidateListItem]
    total: int
    limit: int
    offset: int


class JDIPromoteResponse(BaseModel):
    """Response after promoting a candidate."""
    job_id: int
    status: str = "promoted"


class JDIRunResponse(BaseModel):
    """Response after triggering ingestion."""
    new_candidates: int
    total_emails_scanned: int
    message: str = "Ingestion complete"
