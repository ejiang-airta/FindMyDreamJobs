# ✅ File: app/ai/optimizer.py
#Highlight skills, inject missing keywords
from typing import List
import textwrap
import logging

# Setup the logger
logger = logging.getLogger(__name__)

def optimize_resume_with_skills(resume_text: str, job_description: str, emphasized_skills: List[str], justification: str) -> str:
    """
    AI-enhances a resume by adding a 'Skills Highlight' section with emphasized skills and justification.
    Avoids fabricating experience; only formats and emphasizes existing or user-supported content.
    """
    # Deduplicate and clean emphasized skills
    unique_skills = sorted(set(skill.strip().capitalize() for skill in emphasized_skills if skill.strip()))

    # Format as bullet points
    skill_section = "\n".join(f"- {skill}" for skill in unique_skills)

    # Add formatted justification
    justified_note = textwrap.fill(
        f"As highlighted in the job description, the following skills are critical for success in this role. "
        f"The applicant has provided justification for emphasizing these skills during resume optimization: {justification.strip()}",
        width=80
    )

    # Final enhanced section to be added
    enhancement = f"""
===========================
🔍 AI-Optimized Resume Section
===========================

{justified_note}

⚡ Highlighted Skills:
{skill_section}

===========================
"""

    # Combine the original resume text with the enhancement
    enhanced_resume = f"{resume_text.strip()}\n\n{enhancement.strip()}"
    # Log the optimization process
    logger.debug("Resume optimization completed.")
    logger.info(f"Enhanced resume with {len(unique_skills)} emphasized skills.")
    logger.info(f"Enhancing resume with {len(emphasized_skills)} emphasized skills.")
    logger.info(f"Justification for skills: {justification.strip()}")

    
    # Return the enhanced resume text
    return enhanced_resume

    
