# File: backend/app/services/jdi/scoring.py
# Resume selection and scoring for JDI candidates
import logging
from typing import Optional
from sqlalchemy.orm import Session

from app.models.resume import Resume
from app.models.user_profile import UserProfile
from app.services.score_calc import calculate_scores
from app.utils.job_extraction import extract_skills_with_frequency

logger = logging.getLogger(__name__)


def select_best_resume(
    user_id: int,
    jd_text: str,
    db: Session,
) -> tuple[Optional[int], int]:
    """
    Select the best resume for a JDI candidate and compute the match score.

    Respects user's jdi_resume_select_mode:
    - auto_best: Score JD against all base resumes (up to 3), pick highest match
    - keyword_rules: Match JD text against keyword rules, select mapped resume

    Args:
        user_id: The user ID.
        jd_text: Full job description text.
        db: Database session.

    Returns:
        Tuple of (selected_resume_id, match_score 0-100).
        Returns (None, 0) if no resumes available.
    """
    if not jd_text or not jd_text.strip():
        return None, 0

    # Load user profile for preferences
    profile = db.query(UserProfile).filter_by(user_id=user_id).first()

    # Determine which resumes to score against
    base_resume_ids = None
    select_mode = "auto_best"

    if profile:
        base_resume_ids = profile.jdi_base_resume_ids
        select_mode = profile.jdi_resume_select_mode or "auto_best"

    # Load resumes
    if base_resume_ids:
        resumes = (
            db.query(Resume)
            .filter(Resume.user_id == user_id, Resume.id.in_(base_resume_ids))
            .all()
        )
    else:
        # Fall back to all user resumes (limit 3 most recent)
        resumes = (
            db.query(Resume)
            .filter(Resume.user_id == user_id)
            .order_by(Resume.created_at.desc())
            .limit(3)
            .all()
        )

    if not resumes:
        logger.warning(f"No resumes found for user_id={user_id}")
        return None, 0

    # Extract JD keywords for scoring
    skills_data = extract_skills_with_frequency(jd_text)
    jd_keywords = [s["skill"] for s in skills_data.get("skills", []) if s["skill"] != "N/A"]

    if select_mode == "keyword_rules" and profile and profile.jdi_resume_keyword_rules:
        # Keyword rules mode: match JD text against rules
        resume_id = _apply_keyword_rules(jd_text, profile.jdi_resume_keyword_rules, resumes)
        if resume_id:
            # Score the selected resume
            resume = next((r for r in resumes if r.id == resume_id), None)
            if resume and resume.parsed_text:
                _, match_score, _ = calculate_scores(resume.parsed_text, jd_text, jd_keywords)
                return resume_id, round(match_score)
        # Fall through to auto_best if no rule matched

    # auto_best mode: score all resumes, pick highest
    best_id = None
    best_score = 0

    for resume in resumes:
        if not resume.parsed_text:
            continue
        _, match_score, _ = calculate_scores(resume.parsed_text, jd_text, jd_keywords)
        if match_score > best_score:
            best_score = match_score
            best_id = resume.id

    return best_id, round(best_score)


def _apply_keyword_rules(
    jd_text: str,
    rules: dict,
    resumes: list[Resume],
) -> Optional[int]:
    """
    Apply keyword→resume_id mapping rules.

    Rules format: {"keyword_or_phrase": resume_id, ...}
    First matching rule wins.
    """
    jd_lower = jd_text.lower()
    resume_ids = {r.id for r in resumes}

    for keyword, resume_id in rules.items():
        if keyword.lower() in jd_lower:
            rid = int(resume_id)
            if rid in resume_ids:
                return rid

    return None
