# File: backend/app/services/jdi/ingestion.py
# Main JDI ingestion pipeline orchestrator
import logging
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from typing import Optional, List

from app.models.user_integration import UserIntegration
from app.models.user_profile import UserProfile
from app.models.jdi_candidate import JDICandidate
from app.services.jdi.gmail_oauth import get_gmail_credentials
from app.services.jdi.gmail_scanner import fetch_job_alert_emails, SOURCE_EMAIL_PATTERNS
from app.services.jdi.link_extractor import extract_job_links, resolve_canonical_url, normalize_url
from app.services.jdi.jd_fetcher import fetch_jd_html, extract_jd_text, compute_jd_hash
from app.services.jdi.scoring import select_best_resume
from app.services.jdi.match_reasons import generate_match_reasons
from app.utils.job_extraction import extract_title, extract_company_name, extract_location, extract_salary
from app.models.resume import Resume

logger = logging.getLogger(__name__)


def _detect_source(from_addr: str) -> str:
    """Detect the job source from the sender email address."""
    from_lower = from_addr.lower()
    for source, patterns in SOURCE_EMAIL_PATTERNS.items():
        for pattern in patterns:
            if pattern.lower() in from_lower:
                return source
    return "other"


def run_jdi_ingestion(
    *,
    user_id: int,
    db: Session,
    window_hours: int = 24,
    sources_enabled: Optional[List[str]] = None,
    custom_source_patterns: Optional[List[str]] = None,
) -> dict:
    sources_enabled = sources_enabled or []
    custom_source_patterns = custom_source_patterns or []

    logger.info(
        "JDI ingestion start: user_id=%s window_hours=%s sources_enabled=%s",
        user_id, window_hours, sources_enabled
    )
    """
    Main JDI ingestion pipeline.

    Steps:
    1. Check for active Gmail integration
    2. Load user profile (sources, min score, base resumes)
    3. Fetch job alert emails from Gmail
    4. Extract job links from email HTML
    5. Resolve and canonicalize URLs
    6. Deduplicate against existing candidates
    7. Fetch full JD text from each job page
    8. Extract metadata (title, company, location, salary)
    9. Score against user's base resumes
    10. Generate match reasons
    11. Persist as jdi_candidate records

    Args:
        user_id: The user to run ingestion for.
        db: Database session.
        window_hours: How far back to scan emails.

    Returns:
        Dict with keys: new_candidates, total_emails_scanned, message
    """
    # Step 1: Check for active Gmail integration
    integration = (
        db.query(UserIntegration)
        .filter_by(user_id=user_id, provider="gmail", status="active")
        .first()
    )
    if not integration:
        return {
            "new_candidates": 0,
            "total_emails_scanned": 0,
            "message": "No active Gmail integration. Please connect Gmail first.",
        }

    # Step 2: Load user profile for source filters and preferences
    profile = db.query(UserProfile).filter_by(user_id=user_id).first()
    sources_enabled = profile.jdi_sources_enabled if profile else None
    min_score = profile.jdi_min_score if profile else 60

    # Step 3: Get Gmail credentials and fetch emails
    try:
        credentials = get_gmail_credentials(user_id, db)
    except Exception as e:
        logger.error(f"Failed to get Gmail credentials for user_id={user_id}: {e}")
        # Mark integration as error
        integration.status = "error"
        db.commit()
        return {
            "new_candidates": 0,
            "total_emails_scanned": 0,
            "message": f"Gmail authentication error: {str(e)}",
        }

    emails = fetch_job_alert_emails(
        credentials=credentials,
        sources=sources_enabled,
        window_hours=window_hours,
        custom_patterns=custom_source_patterns,
    )

    total_emails = len(emails)
    if not emails:
        # Update last_sync timestamp even if no emails found
        integration.last_sync_at = datetime.now(timezone.utc)
        db.commit()
        return {
            "new_candidates": 0,
            "total_emails_scanned": 0,
            "message": "No job alert emails found in the specified time window.",
        }

    logger.info(f"Processing {total_emails} emails for user_id={user_id}")

    # Step 4-11: Process each email
    new_candidates = 0

    for email_data in emails:
        source = _detect_source(email_data["from_addr"])
        message_id = email_data["message_id"]

        # Step 4: Extract job links from email HTML
        job_links = extract_job_links(email_data["body_html"], source)
        if not job_links:
            continue

        for raw_url in job_links:
            try:
                new_candidate = _process_single_link(
                    user_id=user_id,
                    raw_url=raw_url,
                    source=source,
                    message_id=message_id,
                    min_score=min_score,
                    db=db,
                )
                if new_candidate:
                    new_candidates += 1
            except Exception as e:
                logger.warning(f"Error processing link {raw_url[:80]}: {e}")
                continue

    # Update last sync timestamp
    integration.last_sync_at = datetime.now(timezone.utc)
    db.commit()

    logger.info(f"JDI ingestion complete: {new_candidates} new candidates from {total_emails} emails")

    return {
        "new_candidates": new_candidates,
        "total_emails_scanned": total_emails,
        "message": "Ingestion complete",
    }


def _process_single_link(
    user_id: int,
    raw_url: str,
    source: str,
    message_id: str,
    min_score: int,
    db: Session,
) -> bool:
    """
    Process a single job link through the full pipeline.
    Returns True if a new candidate was created.
    """
    # Step 5: Resolve and canonicalize URL
    resolved_url = resolve_canonical_url(raw_url)
    canonical_url = normalize_url(resolved_url)

    # Step 6: Deduplicate
    existing = (
        db.query(JDICandidate)
        .filter_by(user_id=user_id, job_url_canonical=canonical_url)
        .first()
    )
    if existing:
        logger.debug(f"Duplicate candidate skipped: {canonical_url[:60]}")
        return False

    # Step 7: Fetch full JD text
    html = fetch_jd_html(resolved_url)
    if not html:
        logger.debug(f"Failed to fetch JD HTML: {resolved_url[:60]}")
        return False

    jd_text, extraction_confidence = extract_jd_text(html, source)
    if not jd_text or extraction_confidence < 30:
        logger.debug(f"Low confidence JD extraction ({extraction_confidence}): {resolved_url[:60]}")
        return False

    jd_hash = compute_jd_hash(jd_text)

    # Check JD hash for duplicates (same JD text from different URLs)
    hash_dup = (
        db.query(JDICandidate)
        .filter_by(user_id=user_id, jd_hash=jd_hash)
        .first()
    )
    if hash_dup:
        logger.debug(f"Duplicate JD hash skipped: {jd_hash[:16]}")
        return False

    # Step 8: Extract metadata
    title = extract_title(jd_text)
    company = extract_company_name(jd_text)
    location = extract_location(jd_text)
    salary = extract_salary(jd_text)

    # Step 9: Score against base resumes
    selected_resume_id, match_score = select_best_resume(user_id, jd_text, db)

    # Apply min_score filter
    if match_score < min_score:
        logger.debug(f"Below min score ({match_score} < {min_score}): {title}")
        return False

    # Step 10: Generate match reasons
    resume_text = ""
    if selected_resume_id:
        resume = db.query(Resume).filter_by(id=selected_resume_id).first()
        if resume:
            resume_text = resume.parsed_text or ""

    match_reasons = generate_match_reasons(
        resume_text=resume_text,
        jd_text=jd_text,
        match_score=match_score,
        jd_title=title,
        jd_location=location,
    )

    # Step 11: Create candidate record
    candidate = JDICandidate(
        user_id=user_id,
        source=source,
        source_message_id=message_id,
        job_url_raw=raw_url,
        job_url_canonical=canonical_url,
        title=title if title != "Unknown Title" else None,
        company=company if company != "Unknown Company" else None,
        location=location if location != "Unspecified" else None,
        salary_text=salary,
        jd_text=jd_text,
        jd_hash=jd_hash,
        jd_extraction_confidence=extraction_confidence,
        match_score=match_score,
        match_reasons=match_reasons,
        selected_resume_id=selected_resume_id,
        status="new",
    )
    db.add(candidate)
    db.flush()

    logger.info(f"New JDI candidate: {title} at {company} (score={match_score})")
    return True
