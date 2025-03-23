# The calculate_ats_score function takes a resume_text string as input and returns a tuple of two integers: before_score and after_score.
import random

def calculate_ats_score(resume_text: str) -> tuple[int, int]:
    parsed = resume_text.lower()

    has_contact = "email" in parsed or "@" in parsed
    has_sections = all(kw in parsed for kw in ["experience", "education", "skills"])
    keyword_density = sum(1 for word in ["python", "sql", "aws", "docker"] if word in parsed)

    base_score = 40
    if has_contact:
        base_score += 10
    if has_sections:
        base_score += 20
    base_score += keyword_density * 5

    before_score = min(base_score, 85)
    after_score = min(before_score + 10 + random.randint(0, 5), 100)

    return before_score, after_score
