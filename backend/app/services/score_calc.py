# ✅ File: /backend/app/services/score_calc.py
# ATS Scoring Engine (Modular & Extensible)

from typing import List, Tuple
import re
from app.config.skills_config import SKILL_KEYWORDS, SECTION_KEYWORDS
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ✨ Define keywords for ATS scoring from config.skills_config:
ATS_KEYWORDS = SKILL_KEYWORDS


# ✅ Check for formatting issues
def check_formatting_rules(resume_text: str) -> List[str]:
    warnings = []

    if len(resume_text) < 500:
        warnings.append("Resume is too short (under 500 characters).")

    if len(resume_text) > 10000:
        warnings.append("Resume may be too long (over 10,000 characters).")

    if not re.search(r"(email|e-mail|@)", resume_text, re.IGNORECASE):
        warnings.append("No email address detected.")

    if not re.search(r"\b(experience|background|history)\b", resume_text, re.IGNORECASE):
        warnings.append("No work experience keywords detected.")

    return warnings


# ✅ Simple keyword coverage score (0–50 range)
def calculate_keyword_score(resume_text: str, keywords: List[str]) -> int:
    resume_text = resume_text.lower()
    matches = [kw for kw in keywords if kw.lower() in resume_text]
    coverage = len(matches) / len(keywords)
    return round(min(coverage * 50, 50))  # max of 50 pts


# ✅ TF-IDF similarity score (0–100)
def calculate_similarity_score(resume_text: str, job_description: str) -> float:
    if not job_description.strip():
        return 0.0

    docs = [resume_text.lower(), job_description.lower()]
    tfidf = TfidfVectorizer().fit_transform(docs)
    similarity = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
    return round(similarity * 100, 2)


# ✅ Match score via skill overlap (0–100)
def calculate_skill_match_score(resume_text: str, jd_keywords: List[str]) -> float:
    resume_text = resume_text.lower()
    matched = [kw for kw in jd_keywords if kw.lower() in resume_text]
    score = round((len(matched) / max(len(jd_keywords), 1)) * 100, 2)
    return float(score)


# ✅ Combined match score (TF-IDF + skill overlap average)
def calculate_match_score(resume_text: str, job_description: str, jd_keywords: List[str]) -> float:
    tfidf_score = calculate_similarity_score(resume_text, job_description)
    keyword_score = calculate_skill_match_score(resume_text, jd_keywords)
    return round((tfidf_score + keyword_score) / 2, 2)


# ✅ Unified scoring entry point (ATS + Match)
def calculate_scores(resume_text: str, job_description: str = "", jd_keywords: List[str] = None) -> Tuple[float, float, List[str]]:
    """
    Returns:
    - ats_score: ATS formatting score (based on resume only, 0-85)
    - match_score: resume/job match score (TF-IDF + keyword overlap, 0-100)
    - warnings: list of improvement suggestions
    """
    if not resume_text or not resume_text.strip():
        return 0.0, 0.0, ["Empty resume text."]

    warnings = check_formatting_rules(resume_text)
    ats_score = min(85, 50 + calculate_keyword_score(resume_text, ATS_KEYWORDS) * 2)

    match_score = 0.0
    if job_description and jd_keywords:
        tfidf_score = calculate_similarity_score(resume_text, job_description)
        keyword_score = calculate_skill_match_score(resume_text, jd_keywords)
        match_score = round((tfidf_score + keyword_score) / 2, 2)

    return float(ats_score), float(match_score), warnings
