# ✅ File: /backend/app/services/ats_scoring.py
# ATS Scoring Engine (Modular & Extensible)
# TODO: decide the best ATS/Match scoring system later.

from typing import List, Tuple, Dict
import re
import random
from typing import List, Tuple
from app.config.skills_config import SKILL_KEYWORDS, ATS_KEYWORDS
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.resume import Resume



# ✨ Define base rules for ATS formatting check
SECTION_KEYWORDS = ["experience", "education", "skills", "summary"]
# ✨ Define keywords for ATS scoring from config.skills_config:
ATS_KEYWORDS = SKILL_KEYWORDS

# ✅ Formatting check

def check_formatting_rules(resume_text: str) -> List[str]:
    warnings = []
    text = resume_text.lower()

    if "@" not in text:
        warnings.append("Missing email/contact information.")
    if not any(kw in text for kw in SECTION_KEYWORDS):
        warnings.append("Missing major resume sections (e.g., Education, Skills, Experience).")
    if text.count(".") / max(len(text.split("\n")), 1) < 0.5:
        warnings.append("Lack of bullet point structure (too few sentences per line).")

    return warnings

# ✅ Keyword-based scoring

def calculate_keyword_score(resume_text: str, keywords: List[str]) -> int:
    resume_text = resume_text.lower()
    return sum(1 for kw in keywords if kw in resume_text)

# ✅ TF-IDF Matching Logic

def calculate_similarity_score(resume_text: str, job_description: str) -> float:
    try:
        tfidf = TfidfVectorizer(stop_words='english')
        vectors = tfidf.fit_transform([resume_text, job_description])
        score = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
        return round(score * 100, 2)
    except Exception:
        return 0.0

# ✅ Main ATS Scoring API (can be swapped easily)

def calculate_ats_score(resume_text: str, job_description: str = "") -> Tuple[int, int, List[str]]:
    """
    Returns:
    - before_score: ATS formatting score (based on resume only)
    - match_score: resume/job match score (TF-IDF + keyword density)
    - warnings: list of improvement suggestions
    """
    if not resume_text or len(resume_text.strip()) == 0:
        return 0, 0, ["Empty resume text"]

    # 🔍 Step 1: Formatting / ATS readiness
    warnings = check_formatting_rules(resume_text)
    # While there's no public open-source standard for ATS scoring, 
    # these numbers mirror what Jobscan and Rezi consider ideal resume structure.
    # 50 is the starting point assuming minimal content
    formatting_score = 50 + calculate_keyword_score(resume_text, ATS_KEYWORDS) * 2
    formatting_score = min(formatting_score, 85)

    # 🔍 Step 2: Match Score (if JD provided)
    match_score = 0
    if job_description:
        match_score = calculate_similarity_score(resume_text, job_description)

    ats_score = formatting_score

    # 🚀 Future: We can add pluggable scorers here

    return float(ats_score), float(match_score), warnings

def update_ats_score(resume_id: int, score: float, db: Session):
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    if resume.ats_score_initial is None:
        resume.ats_score_initial = score

    resume.ats_score_final = score
    db.commit()
    return {
        "ats_score_initial": resume.ats_score_initial,
        "ats_score_final": resume.ats_score_final
    }
def calculate_skill_match_score(resume_text: str, jd_keywords: List[str]) -> float:
    resume_text = resume_text.lower()
    matched = [kw for kw in jd_keywords if kw in resume_text]
    score = round((len(matched) / max(len(jd_keywords), 1)) * 100, 2)
    return float(score)

# ✅ ALL Function below are due to effort to centralize scoring functions:
def calculate_scores(resume_text: str, job_description: str = "", jd_keywords: List[str] = None) -> Tuple[float, float, List[str]]:
    if not resume_text.strip():
        return 0.0, 0.0, ["Empty resume"]

    warnings = check_formatting_rules(resume_text)
    ats_score = min(85, 50 + calculate_keyword_score(resume_text, ATS_KEYWORDS) * 2)

    match_score = 0.0
    if job_description and jd_keywords:
        match_score = calculate_match_score(resume_text, job_description, jd_keywords)

    return float(ats_score), float(match_score), warnings

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

# ✅ Unified scoring entry point (ATS + Match)
def calculate_scores(resume_text: str, job_description: str = "", jd_keywords: List[str] = None) -> Tuple[float, float, List[str]]:
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
def calculate_match_score(resume_text: str, job_description: str, jd_keywords: List[str]) -> float:
    tfidf_score = calculate_similarity_score(resume_text, job_description)
    keyword_score = calculate_skill_match_score(resume_text, jd_keywords)
    return round((tfidf_score + keyword_score) / 2, 2)