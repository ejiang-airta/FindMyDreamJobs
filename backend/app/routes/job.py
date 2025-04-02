# ✅ File: //backend/app/routes/job.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database.connection import get_db
from app.models.job import Job
from datetime import datetime, timezone
import re
import spacy
from app.utils.job_extraction import (
    extract_title,
    extract_company_name,
    extract_skills,
    extract_experience,
    extract_location
)

router = APIRouter()

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

class JobInput(BaseModel):
    job_link: str | None = None
    job_description: str | None = None
    user_id: int  # Required to track which user added this job

@router.post("/parse-job-description", tags=["Jobs"])
async def parse_job_description(job: JobInput, db: Session = Depends(get_db)):
    if not job.job_link and not job.job_description:
        raise HTTPException(status_code=400, detail="Job link or description is required.")

    # 🔍 Use raw text if provided, else fetch from job link (scraper can be added later)
    description = job.job_description or "N/A"

    # 🧠 Basic parsing logic — can be replaced with spaCy or custom model
    skills = extract_skills(description)
    title = extract_title(description)
    experience = extract_experience(description)
    location = extract_location(description)
    company = extract_company_name(description)

    # 🧾 Save to DB
    new_job = Job(
        user_id=job.user_id,
        job_link=job.job_link or "N/A",
        job_description=description,
        job_title=title,
        extracted_skills=skills,
        required_experience=experience,
        company_name=company or "Unknown Company",  # ✅ Fallback if extract company return nothing
        location=location,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    return {
        "message": "✅ Job parsed and saved.",
        "job_id": new_job.id,
        "company": company,
        "title": title,
        "skills": skills,
        "experience": experience,
        "company_name": company,
        "location": location,
    }
# ------------------------------
# 🧠 Utility extractors
# Moved to util/job_extraction.py
# ------------------------------
# ✅ Basic skill extractor (can be replaced with AI model later)
# def extract_skills(text: str):
#     keywords = ["Python", "Django", "FastAPI", "React", "SQL", "AWS", "Kubernetes"]
#     return [kw for kw in keywords if kw.lower() in text.lower()]

# def extract_title(text: str):
#     match = re.search(r"(?i)(software engineer|developer|data scientist|backend engineer)", text)
#     return match.group(0) if match else "Unknown Title"

# def extract_experience(text: str):
#     match = re.search(r"\d+\+?\s+years?", text)
#     return match.group(0) if match else "Unspecified"

# def extract_location(text: str):
#     known_locations = ["Vancouver", "Toronto", "Remote", "San Francisco", "New York", "Seattle", "Austin"]
#     for loc in known_locations:
#         if loc.lower() in text.lower():
#             return loc
#     return None

# def extract_title_nlp(text: str) -> str:
#     # 1️⃣ Primary match: Capture full phrases like "Director of Engineering"
#     primary_match = re.search(
#         r"(?i)\b(?:VP|Vice President|Director|Head|Manager|Lead|CTO|CEO|Engineering Manager|Engineering Director|VP of Engineering|Director of Engineering)\b(?:\s+of\s+\w+)?",
#         text
#     )
#     if primary_match:
#         title = primary_match.group(0)
#         return title.strip()

#     # 2️⃣ Fallback match: lowercase roles (e.g., "backend engineer", "data scientist")
#     fallback_match = re.search(
#         r"(?i)\b(?:backend engineer|frontend engineer|data scientist|software engineer|developer|full stack developer)\b",
#         text
#     )
#     if fallback_match:
#         return fallback_match.group(0).title()

#     # 3️⃣ Nothing found
#     return "Unknown Title"


# def extract_company_nlp(text: str) -> str:
#     """
#     Improved company name extractor based on context phrases.
#     """

#     # Look for known patterns like "Clio is", "Amazon is", etc.
#     match = re.search(r"\b([A-Z][a-zA-Z0-9&\-]+)\s+is\s+(hiring|looking for|seeking)", text)
#     if match:
#         return match.group(1)

#     # Try pattern like "at Clio", "with Amazon"
#     match = re.search(r"\bat\s+([A-Z][a-zA-Z0-9&\-]+)", text)
#     if match:
#         return match.group(1)

#     # Try finding company names from sentence start: "Clio is more than a..."
#     match = re.search(r"^([A-Z][a-zA-Z0-9&\-]+)\s+(is|are)", text)
#     if match:
#         return match.group(1)

#     # As a last fallback, pick the first capitalized word that’s not a title or buzzword
#     words = text.split()
#     blacklist = {"The", "This", "Our", "We", "A", "An", "About", "As", "In"}
#     for word in words:
#         if word.istitle() and word not in blacklist:
#             return word

#     return "Unknown Company"


