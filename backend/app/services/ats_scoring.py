# ✅ File: /backend/app/services/ats_scoring.py
# ATS Scoring Engine (Modular & Extensible)

from typing import List, Tuple, Dict
import re
import random
from app.config.skills_config import SKILL_KEYWORDS
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

    return ats_score, match_score, warnings

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
