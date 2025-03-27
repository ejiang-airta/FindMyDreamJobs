# ✅ File: app/services/resume_optimizer.py
from app.ai.optimizer import optimize_resume_with_skills
import logging

# Setup the logger
logger = logging.getLogger(__name__)


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


