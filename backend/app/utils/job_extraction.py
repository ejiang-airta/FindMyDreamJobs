# File: /backend/app/utils/job_extraction.py
# Utility functions for job extraction
import re
import spacy
from app.config.skills_config import SKILL_KEYWORDS, MIN_SKILL_FREQUENCY, MAX_EMPHASIZED_SKILLS
from collections import Counter
from typing import Optional, Dict, Tuple
from dataclasses import dataclass

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")

# ✅ Extract job title (combined method)
def extract_title(text: str) -> str:
    # 1️⃣ Primary match: Capture full phrases like "Director of Engineering"
    primary_match = re.search(
        r"(?i)\b(?:VP|Vice President|Director|Head|Manager|Lead|CTO|CEO|Engineering Manager|Engineering Director|VP of Engineering|Director of Engineering)\b(?:\s+of\s+\w+)?",
        text
    )
    if primary_match:
        title = primary_match.group(0)
        return title.strip()

    # 2️⃣ Fallback match: lowercase roles (e.g., "backend engineer", "data scientist")
    fallback_match = re.search(
        r"(?i)\b(?:backend engineer|frontend engineer|data scientist|software engineer|developer|full stack developer)\b",
        text
    )
    if fallback_match:
        return fallback_match.group(0).title()

    # 3️⃣ Nothing found
    return "Unknown Title"


# ✅ Extract company name (NER + fallback regex)
def extract_company_name(text: str) -> str:
    """
    Improved company name extractor based on context phrases.
    """

    # Look for known patterns like "Clio is", "Amazon is", etc.
    match = re.search(r"\b([A-Z][a-zA-Z0-9&\-]+)\s+is\s+(hiring|looking for|seeking)", text)
    if match:
        return match.group(1)

    # Try pattern like "at Clio", "with Amazon"
    match = re.search(r"\bat\s+([A-Z][a-zA-Z0-9&\-]+)", text)
    if match:
        return match.group(1)

    # Try finding company names from sentence start: "Clio is more than a..."
    match = re.search(r"^([A-Z][a-zA-Z0-9&\-]+)\s+(is|are)", text)
    if match:
        return match.group(1)

    # As a last fallback, pick the first capitalized word that’s not a title or buzzword
    words = text.split()
    blacklist = {"The", "This", "Our", "We", "A", "An", "About", "As", "In"}
    for word in words:
        if word.istitle() and word not in blacklist:
            return word

    return "Unknown Company"


# ✅ Extract skills from job description summary:
def extract_skills_with_frequency(text: str) -> dict:
    """
    Extracts skills and their frequency from the text based on centralized skill list.
    Returns a dictionary like:
    {
        "skills": [{"skill": "Python", "frequency": 3}, ...],
        "emphasized_skills": ["Python", "AWS", ...]
    }
    """
    text_lower = text.lower()
    skill_counter = Counter()
    # Count exact matches of each skill from SKILL_KEYWORDS
    for skill in SKILL_KEYWORDS:
        occurrences = len(re.findall(r'\b' + re.escape(skill.lower()) + r'\b', text_lower))
        if occurrences > 0:
            skill_counter[skill] = occurrences

    # 🔢 Full skill list sorted by frequency (high → low)
    sorted_skills = sorted(
        [{"skill": skill, "frequency": freq} for skill, freq in skill_counter.items()],
        key=lambda x: x["frequency"],
        reverse=True
    )

    # 🌟 Emphasized = top N skills that meet MIN frequency
    emphasized = [
        s["skill"] for s in sorted_skills if s["frequency"] >= MIN_SKILL_FREQUENCY
    ][:MAX_EMPHASIZED_SKILLS]

    return {
        "skills": sorted_skills or [{"skill": "N/A", "frequency": 0}],
        "emphasized_skills": emphasized or ["N/A"]
    }


# ✅ Extract required experience
def extract_experience(text: str) -> str:
    match = re.search(r"\d+\+?\s+years?", text)
    return match.group(0).strip() if match else "Unspecified"

# ✅ Extract location
def extract_location(text: str) -> str:
    doc = nlp(text)

    # spaCy NER
    for ent in doc.ents:
        if ent.label_ in ["GPE", "LOC"]:  # Countries, cities, states
            return ent.text.strip()

    # Fallback regex
    match = re.search(r"in\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)", text)
    return match.group(1).strip() if match else "Unspecified"

def extract_salary(job_description: str) -> Optional[str]:
    """
    Extract salary information from job description text.
    Returns a string like "$140,000 - $200,000" or "$140,000" if found, else None.
    """
    if not job_description:
        return None

    # Common patterns like: $140,000 - $200,000 or $80K–$100K or $120000/year
    patterns = [
        r"\$\s?\d{2,3}(?:,\d{3})?\s*[-–]\s*\$\s?\d{2,3}(?:,\d{3})?",     # e.g. $140,000 - $200,000
        r"\$\s?\d{2,3}K\s*[-–]\s*\$\s?\d{2,3}K",                         # e.g. $80K–$100K
        r"\$\s?\d{2,3}(?:,\d{3})?\s*(?:per year|annually|/year)",        # e.g. $120,000 per year
        r"\$\s?\d{2,3}K\s*(?:per year|annually|/year)",                  # e.g. $120K per year
        r"\$\s?\d{2,3}(?:,\d{3})?",                                      # fallback: single value like $140,000
        r"\$\s?\d{2,3}K"                                                 # fallback: single value like $120K
    ]

    for pattern in patterns:
        match = re.search(pattern, job_description, re.IGNORECASE)
        if match:
            return match.group(0).strip()

    return None