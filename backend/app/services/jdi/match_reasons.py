# File: backend/app/services/jdi/match_reasons.py
# Generate human-readable match reason bullets for JDI candidates
# Uses NLP (spaCy + keyword extraction), NOT GPT — deterministic & fast
import logging
import re
from typing import Optional

from app.utils.job_extraction import extract_skills_with_frequency
from app.config.skills_config import SKILL_KEYWORDS

logger = logging.getLogger(__name__)

# Seniority-level keywords for alignment detection
SENIORITY_KEYWORDS = {
    "senior": ["senior", "sr.", "sr ", "lead", "principal", "staff"],
    "mid": ["mid-level", "mid level", "intermediate"],
    "junior": ["junior", "jr.", "jr ", "entry-level", "entry level", "associate"],
    "manager": ["manager", "director", "head of", "vp", "vice president"],
}

# Domain/industry keywords
DOMAIN_KEYWORDS = {
    "fintech": ["fintech", "financial", "banking", "payments", "trading"],
    "healthcare": ["healthcare", "health tech", "medical", "clinical", "hipaa"],
    "e-commerce": ["e-commerce", "ecommerce", "retail", "marketplace", "shopify"],
    "saas": ["saas", "b2b", "enterprise software", "platform"],
    "ai/ml": ["machine learning", "deep learning", "nlp", "computer vision", "ai"],
    "cloud": ["aws", "gcp", "azure", "cloud", "infrastructure"],
    "devops": ["devops", "sre", "ci/cd", "kubernetes", "docker", "terraform"],
}


def generate_match_reasons(
    resume_text: str,
    jd_text: str,
    match_score: int,
    jd_title: Optional[str] = None,
    jd_location: Optional[str] = None,
) -> list[str]:
    """
    Generate 2-4 concise match reason bullets for a JDI candidate.

    All analysis is deterministic (no GPT calls).

    Args:
        resume_text: Parsed resume text.
        jd_text: Full job description text.
        match_score: The computed match score (0-100).
        jd_title: Extracted job title (optional, for seniority matching).
        jd_location: Extracted location (optional, for location matching).

    Returns:
        List of 2-4 short bullet strings.
    """
    reasons = []

    if not resume_text or not jd_text:
        return ["Match score based on available information"]

    resume_lower = resume_text.lower()
    jd_lower = jd_text.lower()

    # 1. Skill overlap (most important reason)
    skill_reason = _get_skill_overlap_reason(resume_lower, jd_lower)
    if skill_reason:
        reasons.append(skill_reason)

    # 2. Seniority alignment
    seniority_reason = _get_seniority_reason(resume_lower, jd_lower, jd_title)
    if seniority_reason:
        reasons.append(seniority_reason)

    # 3. Domain/industry match
    domain_reason = _get_domain_reason(resume_lower, jd_lower)
    if domain_reason:
        reasons.append(domain_reason)

    # 4. Location/remote compatibility
    location_reason = _get_location_reason(resume_lower, jd_lower, jd_location)
    if location_reason:
        reasons.append(location_reason)

    # Ensure at least 2 reasons with fallbacks
    fallbacks = []
    if match_score >= 70:
        fallbacks = ["Strong overall profile alignment", "Relevant experience for this role"]
    elif match_score >= 50:
        fallbacks = ["Moderate profile alignment with this role", "Some relevant experience detected"]
    else:
        fallbacks = ["Some relevant experience detected", "Potential fit worth reviewing"]

    while len(reasons) < 2 and fallbacks:
        fallback = fallbacks.pop(0)
        if fallback not in reasons:
            reasons.append(fallback)

    # Cap at 4 reasons
    return reasons[:4]


def _get_skill_overlap_reason(resume_lower: str, jd_lower: str) -> Optional[str]:
    """Find top matching skills between resume and JD."""
    jd_skills = extract_skills_with_frequency(jd_lower)
    jd_skill_list = [s["skill"] for s in jd_skills.get("skills", []) if s["skill"] != "N/A"]

    if not jd_skill_list:
        return None

    matching_skills = []
    for skill in jd_skill_list:
        if skill.lower() in resume_lower:
            matching_skills.append(skill)

    if not matching_skills:
        return None

    top_skills = matching_skills[:5]
    if len(top_skills) >= 3:
        return f"Strong skill match: {', '.join(top_skills[:3])} + {len(top_skills) - 3} more"
    elif len(top_skills) == 2:
        return f"Key skills match: {' and '.join(top_skills)}"
    else:
        return f"Relevant skill: {top_skills[0]}"


def _get_seniority_reason(
    resume_lower: str,
    jd_lower: str,
    jd_title: Optional[str] = None,
) -> Optional[str]:
    """Check if seniority levels align between resume and JD."""
    jd_check = (jd_title or "").lower() + " " + jd_lower[:500]

    resume_level = _detect_seniority(resume_lower)
    jd_level = _detect_seniority(jd_check)

    if resume_level and jd_level:
        if resume_level == jd_level:
            level_labels = {
                "senior": "Senior-level",
                "mid": "Mid-level",
                "junior": "Entry-level",
                "manager": "Management-level",
            }
            return f"{level_labels.get(resume_level, resume_level.title())} experience aligns with role"
    return None


def _detect_seniority(text: str) -> Optional[str]:
    """Detect the most prominent seniority level in text."""
    for level, keywords in SENIORITY_KEYWORDS.items():
        for kw in keywords:
            if kw in text:
                return level
    return None


def _get_domain_reason(resume_lower: str, jd_lower: str) -> Optional[str]:
    """Check for shared industry/domain keywords."""
    shared_domains = []

    for domain, keywords in DOMAIN_KEYWORDS.items():
        resume_has = any(kw in resume_lower for kw in keywords)
        jd_has = any(kw in jd_lower for kw in keywords)
        if resume_has and jd_has:
            shared_domains.append(domain)

    if shared_domains:
        return f"Relevant domain experience: {', '.join(shared_domains[:2])}"
    return None


def _get_location_reason(
    resume_lower: str,
    jd_lower: str,
    jd_location: Optional[str] = None,
) -> Optional[str]:
    """Check for location/remote compatibility."""
    jd_check = (jd_location or "").lower() + " " + jd_lower[:1000]

    if re.search(r"\b(remote|work from home|wfh|fully remote)\b", jd_check):
        return "Remote-friendly position"

    if re.search(r"\b(hybrid)\b", jd_check):
        return "Hybrid work arrangement available"

    return None
