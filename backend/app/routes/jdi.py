# File: backend/app/routes/jdi.py
# API routes for JDI (Job Daily Intelligence) candidate feed and actions
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.database.connection import SessionLocal
from app.models.jdi_candidate import JDICandidate
from app.models.job import Job
from app.models.saved_job import SavedJob
from app.models.user_profile import UserProfile
from app.schemas.jdi import (
    JDICandidateListItem,
    JDICandidateDetail,
    JDICandidateFeed,
    JDIPromoteRequest,
    JDIPromoteResponse,
    JDIRunRequest,
    JDIRunResponse,
)
from app.services.jdi.ingestion import run_jdi_ingestion
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/jdi", tags=["JDI"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/candidates", response_model=JDICandidateFeed)
def get_candidates(
    user_id: int = Query(...),
    status: str = Query(default=None),
    min_score: int = Query(default=None, ge=0, le=100),
    unread_only: bool = Query(default=False),
    read_only: bool = Query(default=False),
    source: str = Query(default=None),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
):
    """
    Get paginated JDI candidate feed with optional filters.
    Sorted by match_score descending.
    """
    query = db.query(JDICandidate).filter(JDICandidate.user_id == user_id)

    if status:
        query = query.filter(JDICandidate.status == status)
    else:
        # Default: show new candidates
        query = query.filter(JDICandidate.status == "new")

    if min_score is not None:
        query = query.filter(JDICandidate.match_score >= min_score)

    if unread_only:
        query = query.filter(JDICandidate.seen_at.is_(None))
    elif read_only:
        query = query.filter(JDICandidate.seen_at.isnot(None))

    if source:
        query = query.filter(JDICandidate.source == source)

    total = query.count()
    candidates = (
        query
        .order_by(desc(JDICandidate.match_score))
        .offset(offset)
        .limit(limit)
        .all()
    )

    return JDICandidateFeed(
        candidates=[JDICandidateListItem.model_validate(c) for c in candidates],
        total=total,
        limit=limit,
        offset=offset,
    )


@router.get("/candidates/{candidate_id}", response_model=JDICandidateDetail)
def get_candidate_detail(
    candidate_id: str,
    user_id: int = Query(...),
    db: Session = Depends(get_db),
):
    """Get full details for a single JDI candidate."""
    candidate = (
        db.query(JDICandidate)
        .filter_by(id=candidate_id, user_id=user_id)
        .first()
    )
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return candidate


@router.post("/candidates/{candidate_id}/mark-seen")
def mark_candidate_seen(
    candidate_id: str,
    user_id: int = Query(...),
    db: Session = Depends(get_db),
):
    """Mark a candidate as seen (read)."""
    candidate = (
        db.query(JDICandidate)
        .filter_by(id=candidate_id, user_id=user_id)
        .first()
    )
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")

    candidate.seen_at = datetime.now(timezone.utc)
    db.commit()
    return {"status": "seen", "candidate_id": candidate_id}


@router.post("/candidates/{candidate_id}/ignore")
def ignore_candidate(
    candidate_id: str,
    user_id: int = Query(...),
    db: Session = Depends(get_db),
):
    """Set a candidate's status to ignored."""
    candidate = (
        db.query(JDICandidate)
        .filter_by(id=candidate_id, user_id=user_id)
        .first()
    )
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")

    candidate.status = "ignored"
    db.commit()
    return {"status": "ignored", "candidate_id": candidate_id}


@router.post("/candidates/{candidate_id}/promote", response_model=JDIPromoteResponse)
def promote_candidate(
    candidate_id: str,
    body: JDIPromoteRequest,
    user_id: int = Query(...),
    db: Session = Depends(get_db),
):
    """
    Promote a JDI candidate to a Job record.

    Option A (from TDD): Always create a new Job record.
    - mode=save: Also create SavedJob record
    - mode=analyze: Return job_id for frontend to navigate to /analyze?job_id={id}
    """
    candidate = (
        db.query(JDICandidate)
        .filter_by(id=candidate_id, user_id=user_id)
        .first()
    )
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")

    if candidate.status == "promoted":
        raise HTTPException(status_code=400, detail="Candidate already promoted")

    # Step 1: Create Job record from candidate data
    job = Job(
        user_id=user_id,
        job_title=candidate.title or "Untitled Position",
        company_name=candidate.company or "Unknown Company",
        location=candidate.location,
        job_description=candidate.jd_text or "",
        job_link=candidate.job_url_raw,
        salary=candidate.salary_text,
    )
    db.add(job)
    db.flush()  # Get the job.id

    # Step 2: If mode=save, also create SavedJob
    if body.mode == "save":
        saved_job = SavedJob(
            user_id=user_id,
            search_id=f"jdi-{candidate.id}",
            job_title=job.job_title,
            employer_name=job.company_name,
            job_location=job.location,
            job_salary=job.salary,
            job_description=job.job_description,
            job_apply_link=candidate.job_url_raw or "",
            job_posted_at=candidate.created_at,
        )
        db.add(saved_job)

    # Step 3: Update candidate status
    candidate.status = "promoted"
    db.commit()

    logger.info(f"Promoted candidate {candidate_id} → job_id={job.id} (mode={body.mode})")

    return JDIPromoteResponse(job_id=job.id, status="promoted")


@router.post("/run", response_model=JDIRunResponse)
def run_ingestion(
    body: JDIRunRequest = None,
    user_id: int = Query(...),
    db: Session = Depends(get_db),
):
    """
    Trigger JDI ingestion: scan Gmail for job alerts, extract, score, and persist.
    """
    body = body or JDIRunRequest()  # ensures fields exist if request body omitted

    # Load user profile to get scan window and custom sources
    profile = db.query(UserProfile).filter_by(user_id=user_id).first()

    # Get scan window from profile (default 7 days = 168 hours)
    scan_window_days = profile.jdi_scan_window_days if profile else 7
    window_hours = scan_window_days * 24

    # Override with request body if provided (for backward compatibility)
    if body.window_hours:
        try:
            window_hours = int(body.window_hours)
        except (TypeError, ValueError):
            pass

    # Get sources from profile or request
    sources_enabled = getattr(body, "sources_enabled", None) or []
    if not isinstance(sources_enabled, list):
        sources_enabled = []
    sources_enabled = [str(s).strip() for s in sources_enabled if str(s).strip()]

    # Get custom source patterns from profile
    custom_source_patterns = profile.jdi_custom_source_patterns if profile else None

    logger.info(
        "JDI run: user_id=%s window_hours=%s sources_enabled=%s custom_patterns=%s",
        user_id, window_hours, sources_enabled, custom_source_patterns
    )

    try:
        result = run_jdi_ingestion(
            user_id=user_id,
            db=db,
            window_hours=window_hours,
            sources_enabled=sources_enabled,
            custom_source_patterns=custom_source_patterns,
        )
        return JDIRunResponse(**result)
    except Exception as e:
        logger.exception("JDI ingestion error for user_id=%s", user_id)
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {str(e)}")

