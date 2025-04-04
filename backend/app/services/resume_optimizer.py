# ✅ File: app/services/resume_optimizer.py
from app.ai.optimizer import optimize_resume_with_skills
import logging

# Setup the logger
logger = logging.getLogger("app")


# This acts as a pass-through for now, but can evolve in future
def optimize_resume_with_skills_service(resume_text: str, job_description: str, emphasized_skills: list[str], justification: str) -> str:
    # Log the optimization process:
    logger.debug("Delegating optimization to AI logic layer.")
    logger.info(f"Optimizing resume with {len(emphasized_skills)} emphasized skills.")
   
    return optimize_resume_with_skills(
        resume_text=resume_text,
        job_description=job_description,
        emphasized_skills=emphasized_skills,
        justification=justification
    )

def optimize_resume_for_job(resume_text: str, job_skills: list[str], emphasized_skills: list[str]) -> str:
    highlighted_resume = resume_text

    # Sort skills by length to avoid partial overlaps
    sorted_skills = sorted(set(job_skills), key=len, reverse=True)

    for skill in sorted_skills:
        if skill.lower() in resume_text.lower():
            # Check if this is emphasized
            if skill in emphasized_skills:
                replacement = f"**{skill.upper()}**"
            else:
                replacement = f"*{skill}*"
            highlighted_resume = re.sub(rf"\b{re.escape(skill)}\b", replacement, highlighted_resume, flags=re.IGNORECASE)

    return highlighted_resume



