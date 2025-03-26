import re
import random

# ✅ Function: Calculate ATS Score (Before & After)
def calculate_ats_score(resume_text: str):
    """
    Calculate ATS score based on resume text.
    Returns: (before_score, after_score)
    """

    if not resume_text or len(resume_text.strip()) == 0:
        return 0, 0  # If empty resume, return zero scores

    resume_text = resume_text.lower()

    # ✅ Basic Checks
    has_contact = "email" in resume_text or "@" in resume_text
    has_sections = all(kw in resume_text for kw in ["experience", "education", "skills"])

    # ✅ Count Keyword Density (Customize as needed)
    ats_keywords = ["python", "sql", "aws", "docker", "fastapi", "react", "node", "git"]
    keyword_density = sum(1 for word in ats_keywords if word in resume_text)

    # ✅ Base Scoring Logic
    base_score = 40
    if has_contact:
        base_score += 10
    if has_sections:
        base_score += 20
    base_score += keyword_density * 5

    before_score = min(base_score, 85)  # ✅ Cap score at 85%
    after_score = min(before_score + 10 + random.randint(0, 5), 100)  # ✅ Fake improvement

    return before_score, after_score