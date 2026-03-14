# File: backend/app/services/jdi/ingestion.py
# Main JDI ingestion pipeline orchestrator
#
# Hybrid strategy:
#  • LinkedIn / Indeed / TrueUp → parse job info directly from email HTML.
#    These sites block scrapers (403 / login redirect), so URL fetching always
#    fails. The alert email already contains title, company, location, salary,
#    snippet, and the apply link — enough to score and surface a candidate.
#  • "Other" sources (Talent.com, Trabajo.org, etc.) → ALSO try to fetch the
#    full job description from the URL for richer scoring text. Falls back to
#    email content automatically if the fetch fails or returns low confidence.
import logging
import re
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from typing import Optional, List

from app.models.user_integration import UserIntegration
from app.models.user_profile import UserProfile
from app.models.jdi_candidate import JDICandidate
from app.services.jdi.gmail_oauth import get_gmail_credentials
from app.services.jdi.gmail_scanner import fetch_job_alert_emails, SOURCE_EMAIL_PATTERNS
from app.services.jdi.email_parser import parse_job_cards, EmailJobCard
from app.services.jdi.link_extractor import normalize_url, resolve_canonical_url
from app.services.jdi.jd_fetcher import fetch_jd_html, extract_jd_text, compute_jd_hash
from app.services.jdi.scoring import select_best_resume
from app.services.jdi.match_reasons import generate_match_reasons
from app.models.resume import Resume

# Sources that block scraping — use email content only for these
_EMAIL_ONLY_SOURCES = {"linkedin", "indeed", "trueup"}

# Email-based content (title+company+location) yields lower TF-IDF scores than
# full job descriptions. Cap the effective min_score for email-only sources so
# relevant jobs aren't filtered out purely because the text is thin.
# Set to 8 — measured against realistic email content:
#   Relevant QA/Mgmt jobs score 11–21% with thin email text.
#   Clearly unrelated jobs (robotics technician, construction, truck driver) score 0–4%.
#   Threshold=8 captures all relevant jobs while filtering true garbage.
_EMAIL_ONLY_MIN_SCORE_CAP = 8

logger = logging.getLogger(__name__)

# Common VP aliases — when user sets "VP" as a target keyword, also match these.
_VP_ALIASES = ["vice president", "v.p."]


def _parse_target_role_keywords(target_titles: Optional[list]) -> list[str]:
    """
    Expand profile.target_titles into a flat list of lowercase keywords.

    The UI stores a single comma-separated string, e.g. ["Manager, Director, VP"].
    We split on commas, strip whitespace, and expand VP → vice-president aliases.

    VP expansion fires when the *first word* of the keyword is "vp", so both
    "VP" and "VP of Engineering" expand to include the vice president aliases.

    Returns [] if no target titles configured (meaning: no filter applied).
    """
    if not target_titles:
        return []
    keywords = []
    for entry in target_titles:
        for kw in str(entry).split(","):
            kw = kw.strip().lower()
            if kw:
                keywords.append(kw)
                # Expand when "vp" is the whole keyword or the leading word
                # (e.g. "vp" → also match "vice president", "v.p."
                #  "vp of engineering" → same aliases cover the VP seniority)
                first_word = kw.split()[0] if kw else ""
                if first_word == "vp":
                    keywords.extend(_VP_ALIASES)
    return keywords


def _title_matches_target_roles(title: Optional[str], keywords: list[str]) -> bool:
    """
    Return True if the job title contains at least one target-role keyword as a
    whole word (or phrase), or if no keywords are configured (filter disabled).

    Uses word-boundary matching so "manager" does NOT match "management" or
    "project management consultant", but DOES match "Engineering Manager".
    Multi-word phrases (e.g. "vice president") are matched as a whole phrase.
    """
    if not keywords:
        return True   # no filter configured — accept all
    if not title:
        return False  # title-less card filtered when keywords are set
    title_lower = title.lower()
    return any(
        re.search(r"\b" + re.escape(kw) + r"\b", title_lower)
        for kw in keywords
    )


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
    force_full_window: bool = False,
) -> dict:
    """
    Main JDI ingestion pipeline.

    Steps:
    1.  Check for active Gmail integration
    2.  Load user profile (sources, min score)
    3.  Get Gmail credentials
    4.  Fetch job alert emails from Gmail
    5.  For each email: parse job cards from email HTML  ← key change
    6.  Deduplicate cards against existing candidates
    7.  Score each card's text against user's base resumes
    8.  Generate match reasons
    9.  Persist as jdi_candidate records

    Args:
        user_id: The user to run ingestion for.
        db: Database session.
        window_hours: How far back to scan emails.
        sources_enabled: Override source list (normally read from profile).
        custom_source_patterns: Additional sender patterns.
        force_full_window: If True, skip the smart incremental window optimisation
            and use window_hours as-is. Set when the caller explicitly requested a
            specific window (e.g. a forced full re-scan from the API).

    Returns:
        Dict with keys: new_candidates, total_emails_scanned, message
    """
    sources_enabled = sources_enabled or []
    custom_source_patterns = custom_source_patterns or []

    logger.info(
        "JDI ingestion start: user_id=%s window_hours=%s sources_enabled=%s",
        user_id, window_hours, sources_enabled,
    )

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

    # Parse target-role keywords for title filtering (e.g. "Manager, Director, VP")
    # Empty list = filter disabled (accept all titles)
    target_role_keywords = _parse_target_role_keywords(
        profile.target_titles if profile else None
    )
    if target_role_keywords:
        logger.info(
            "Target-role filter active: %s",
            ", ".join(target_role_keywords),
        )

    # Step 2b: Smart incremental window — only re-fetch emails since the last sync.
    #
    # Without this, every daily scan re-fetches the full 7-day window, causing:
    #   • Unnecessary Gmail API quota usage (fetching emails already processed)
    #   • Slower ingestion (more emails to parse and deduplicate)
    #
    # Logic:
    #   - Skipped entirely when force_full_window=True (caller requested a specific
    #     window, e.g. a forced full re-scan from the API — honour it exactly).
    #   - First scan (no last_sync_at): use the full configured window_hours.
    #   - Subsequent scans: scan from (last_sync_at - 2h overlap buffer) to now.
    #     The 2h buffer guards against emails delivered during the previous scan run.
    #   - The deduplication layers (URL, title+company, hash) are still the safety
    #     net — the window is an efficiency optimisation, not a correctness gate.
    #   - Floor at 24h so the Gmail newer_than:Xd query always has a valid value.
    if not force_full_window and integration.last_sync_at:
        now_utc = datetime.now(timezone.utc)
        last_sync = integration.last_sync_at
        if last_sync.tzinfo is None:
            last_sync = last_sync.replace(tzinfo=timezone.utc)
        hours_since_last_sync = (now_utc - last_sync).total_seconds() / 3600
        if hours_since_last_sync < 0:
            logger.warning(
                "last_sync_at is in the future (%.1fh ahead) — clock skew? "
                "Falling back to full window.",
                -hours_since_last_sync,
            )
        else:
            # +2h overlap buffer; floor at 24h (Gmail's minimum meaningful unit)
            smart_hours = max(24, int(hours_since_last_sync) + 2)
            if smart_hours < window_hours:
                logger.info(
                    "Smart window: %.1fh since last sync → scanning %dh (was %dh)",
                    hours_since_last_sync, smart_hours, window_hours,
                )
                window_hours = smart_hours
            # else: large gap since last sync — keep the full window_hours

    # Step 3: Get Gmail credentials (raises on auth failure → caught below)
    try:
        credentials = get_gmail_credentials(user_id, db)
    except Exception as e:
        logger.error(f"Failed to get Gmail credentials for user_id={user_id}: {e}")
        integration.status = "error"
        db.commit()
        return {
            "new_candidates": 0,
            "total_emails_scanned": 0,
            "message": f"Gmail authentication error: {str(e)}",
        }

    # Step 4: Fetch job alert emails from Gmail
    # Re-raise Gmail API errors so they surface as auth errors rather than "0 emails".
    try:
        emails = fetch_job_alert_emails(
            credentials=credentials,
            sources=sources_enabled,
            window_hours=window_hours,
            custom_patterns=custom_source_patterns,
        )
    except Exception as e:
        logger.error(f"Gmail API error for user_id={user_id}: {e}")
        integration.status = "error"
        db.commit()
        return {
            "new_candidates": 0,
            "total_emails_scanned": 0,
            "message": f"Gmail API error: {str(e)}",
        }

    total_emails = len(emails)
    if not emails:
        integration.last_sync_at = datetime.now(timezone.utc)
        db.commit()
        return {
            "new_candidates": 0,
            "total_emails_scanned": 0,
            "message": "No job alert emails found in the specified time window.",
        }

    logger.info(f"Processing {total_emails} emails for user_id={user_id}")

    # Steps 5-9: Process each email
    new_candidates = 0

    for email_data in emails:
        source = _detect_source(email_data["from_addr"])
        message_id = email_data["message_id"]

        # Step 5: Parse job cards directly from email HTML (no URL fetching)
        # Include the email subject as scoring context — it contains the alert
        # keyword (e.g. "Head of QA in Vancouver") which boosts TF-IDF relevance.
        cards = parse_job_cards(
            email_data["body_html"],
            source,
            email_subject=email_data.get("subject", ""),
        )
        if not cards:
            logger.debug(f"No job cards parsed from {source} email {message_id[:12]}")
            continue

        for card in cards:
            try:
                created = _process_card(
                    user_id=user_id,
                    card=card,
                    message_id=message_id,
                    min_score=min_score,
                    target_role_keywords=target_role_keywords,
                    db=db,
                )
                if created:
                    new_candidates += 1
            except Exception as e:
                logger.warning(f"Error processing card '{card.title}': {e}")
                continue

    # Update last sync timestamp
    integration.last_sync_at = datetime.now(timezone.utc)
    db.commit()

    logger.info(
        "JDI ingestion complete: %s new candidates from %s emails",
        new_candidates, total_emails,
    )

    return {
        "new_candidates": new_candidates,
        "total_emails_scanned": total_emails,
        "message": "Ingestion complete",
    }


def _process_card(
    user_id: int,
    card: EmailJobCard,
    message_id: str,
    min_score: int,
    db: Session,
    target_role_keywords: Optional[list] = None,
) -> bool:
    """
    Process a single EmailJobCard through scoring and persistence.

    For email-only sources (LinkedIn, Indeed, TrueUp): scores against email
    content (title + company + location + salary + snippet).

    For "other" sources (Talent.com, Trabajo.org, etc.): additionally tries to
    fetch the full job description from the URL. Uses the richer fetched text
    if successful; falls back to email content automatically.

    Returns True if a new candidate was created.
    """
    # Step 5b: Target-role title filter — reject jobs whose title doesn't
    # contain any of the user's target role keywords (e.g. Manager/Director/VP).
    # This runs before URL fetching and scoring so irrelevant jobs are fast-rejected.
    if not _title_matches_target_roles(card.title, target_role_keywords or []):
        logger.debug(
            "Title filter rejected (no target-role match): '%s'",
            card.title or "(no title)",
        )
        return False

    # Canonicalize the apply link for deduplication
    canonical_url = normalize_url(card.apply_link)

    # Step 6: Deduplicate by canonical URL
    existing = (
        db.query(JDICandidate)
        .filter_by(user_id=user_id, job_url_canonical=canonical_url)
        .first()
    )
    if existing:
        logger.debug(f"Duplicate candidate skipped: {canonical_url[:60]}")
        return False

    # Step 6b: Title + company dedup — catches the same job appearing in multiple
    # LinkedIn alert emails (different subject/tracking URLs, same posting).
    # URL dedup catches exact-URL dupes; this catches variant URLs for the same job.
    if card.title and card.company:
        title_co_dup = (
            db.query(JDICandidate)
            .filter_by(user_id=user_id, title=card.title, company=card.company)
            .first()
        )
        if title_co_dup:
            logger.debug(f"Duplicate title+company skipped: {card.title} @ {card.company}")
            return False

    # Determine scoring text and confidence
    # Start with email content (always available)
    email_text = card.to_scoring_text()
    if not email_text.strip():
        logger.debug(f"Empty scoring text for card: {card.apply_link[:60]}")
        return False

    scoring_text = email_text
    extraction_confidence = 80  # Email-sourced baseline

    # For "other" sources, try to fetch the full JD from the URL for richer text
    if card.source not in _EMAIL_ONLY_SOURCES:
        try:
            resolved_url = resolve_canonical_url(card.apply_link)
            html = fetch_jd_html(resolved_url)
            if html:
                fetched_text, fetched_confidence = extract_jd_text(html, card.source)
                if fetched_text and fetched_confidence >= 60:
                    # Use richer fetched text; merge in email metadata if missing
                    scoring_text = fetched_text
                    extraction_confidence = fetched_confidence
                    logger.debug(
                        f"Used fetched JD (confidence={fetched_confidence}) "
                        f"for {card.apply_link[:60]}"
                    )
                else:
                    logger.debug(
                        f"Fetched JD too low confidence ({fetched_confidence}), "
                        f"using email content for {card.apply_link[:60]}"
                    )
        except Exception as e:
            # URL fetch failed — fall back to email content silently
            logger.debug(f"URL fetch failed for {card.apply_link[:60]}: {e}")

    # Dedup by content hash (catches same job appearing in multiple emails)
    jd_hash = compute_jd_hash(scoring_text)
    hash_dup = (
        db.query(JDICandidate)
        .filter_by(user_id=user_id, jd_hash=jd_hash)
        .first()
    )
    if hash_dup:
        logger.debug(f"Duplicate content hash skipped: {jd_hash[:16]}")
        return False

    # Step 7: Score against base resumes
    selected_resume_id, match_score = select_best_resume(user_id, scoring_text, db)

    # For email-only sources (thin content), cap the effective min_score at
    # _EMAIL_ONLY_MIN_SCORE_CAP. Email text (title+company+location) gives lower
    # TF-IDF scores than a full job description, so 60% would filter out
    # relevant jobs. The user sees scores in the UI and can ignore low ones.
    effective_min = (
        min(min_score, _EMAIL_ONLY_MIN_SCORE_CAP)
        if card.source in _EMAIL_ONLY_SOURCES
        else min_score
    )
    if match_score < effective_min:
        logger.debug(
            f"Below min score ({match_score} < {effective_min}): {card.title or card.apply_link[:50]}"
        )
        return False

    # Step 8: Generate match reasons
    resume_text = ""
    if selected_resume_id:
        resume = db.query(Resume).filter_by(id=selected_resume_id).first()
        if resume:
            resume_text = resume.parsed_text or ""

    match_reasons = generate_match_reasons(
        resume_text=resume_text,
        jd_text=scoring_text,
        match_score=match_score,
        jd_title=card.title or "",
        jd_location=card.location or "",
    )

    # Step 9: Persist candidate
    candidate = JDICandidate(
        user_id=user_id,
        source=card.source,
        source_message_id=message_id,
        job_url_raw=card.apply_link,
        job_url_canonical=canonical_url,
        title=card.title,
        company=card.company,
        location=card.location,
        salary_text=card.salary_text,
        jd_text=scoring_text,
        jd_hash=jd_hash,
        jd_extraction_confidence=extraction_confidence,
        match_score=match_score,
        match_reasons=match_reasons,
        selected_resume_id=selected_resume_id,
        status="new",
    )
    db.add(candidate)
    db.flush()

    logger.info(f"New JDI candidate: {card.title} at {card.company} (score={match_score})")
    return True
