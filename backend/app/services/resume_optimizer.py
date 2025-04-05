# ✅ File: app/services/resume_optimizer.py
# Resume Optimization Service
# This module provides a service to optimize resumes using AI and static formatting.
# It includes functions to enhance resumes with job-specific skills and justifications.
# It uses OpenAI's GPT-4ofor AI-based optimization and a static formatter as a fallback.

import logging
from typing import List, Tuple
from openai import OpenAI
import os
import re

# Setup logger
logger = logging.getLogger("app")
client = OpenAI()

# Load OpenAI API key from environment variable
client.api_key = os.getenv("OPENAI_API_KEY")


def optimize_resume_with_skills_service(
    resume_text: str,
    matched_skills: List[str],
    missing_skills: List[str],
    emphasized_skills: List[str],
    justification: str
) -> Tuple[str, List[str]]:
    """
    Primary service function to optimize a resume using GPT-4o.
    Returns: optimized_text, changes_summary
    Only missing skills mentioned in justification will be allowed to be added.
    """
    logger.info(f"Optimizing resume with {len(emphasized_skills)} emphasized skills.")

    try:
        return _optimize_with_gpt(resume_text, matched_skills, missing_skills, emphasized_skills, justification)
    except Exception as e:
        logger.error(f"Resume optimization failed: {e}")
        raise


def _optimize_with_gpt(
    resume_text: str,
    matched_skills: List[str],
    missing_skills: List[str],
    emphasized_skills: List[str],
    justification: str
) -> Tuple[str, List[str]]:
    """
    Uses OpenAI GPT to rewrite the resume.
    """
    matched_str = ", ".join(matched_skills)
    emphasized_str = ", ".join(emphasized_skills)

    # Only keep missing skills that appear in the justification
    allowed_missing_skills = [s for s in missing_skills if s.lower() in justification.lower()]
    missing_str = ", ".join(allowed_missing_skills)


    prompt = f"""
You are a professional resume editor. Given a user's resume, your job is to optimize it by enhancing its language, formatting, and emphasis based on job-specific skills and user justification.

Matched Skills (already present in the resume): {matched_str}
Emphasized Skills (important for this job): {emphasized_str}
User Justification: {justification}

Only incorporate missing skills {missing_str} if they are mentioned or justified explicitly in the justification section. Do not fabricate experience. Be ATS-friendly and highlight achievements where possible.

Original Resume:
{resume_text}

---

Please return two sections:
1. Optimized Resume (rewrite and enhance the original).
2. Bullet list summary of key changes and optimizations you made.

Format your answer like this:
===========================
Optimized Resume:
[...new rewritten resume...]

Changes Summary:
- [...]
- [...]
===========================
"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful and precise resume rewriting assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=1500
    )

    result_text = response.choices[0].message.content
    logger.info("🔍 GPT Response:\n" + result_text)

    optimized_text = ""
    changes_summary = []

    if "Optimized Resume:" in result_text and "Changes Summary:" in result_text:
        parts = result_text.split("Changes Summary:")
        optimized_part = parts[0].split("Optimized Resume:")[-1].strip()
        summary_part = parts[1].strip()
        optimized_text = optimized_part
        changes_summary = [line.strip("- ").strip() for line in summary_part.splitlines() if line.strip().startswith("-")]


    if not optimized_text:
        optimized_text = result_text.strip()  # fallback to full text
        changes_summary = ["⚠️ GPT response format not detected — full response shown."]
        raise ValueError("GPT did not return a valid optimized resume.")

    return optimized_text, changes_summary


# def _fallback_static_formatter(
#     resume_text: str,
#     emphasized_skills: List[str],
#     justification: str
# ) -> Tuple[str, List[str]]:
#     """
#     Static fallback logic to add a justified section to the resume.
#     """
#     unique_skills = sorted(set(skill.strip().capitalize() for skill in emphasized_skills if skill.strip()))
#     skill_section = "\n".join(f"- {skill}" for skill in unique_skills)

#     justified_note = textwrap.fill(
#         f"As highlighted in the job description, the following skills are critical for success in this role. "
#         f"The applicant has provided justification for emphasizing these skills during resume optimization: {justification.strip()}",
#         width=80
#     )

#     enhancement = f"""
# ===========================
# 🔍 AI-Optimized Resume Section
# ===========================

# {justified_note}

# ⚡ Highlighted Skills:
# {skill_section}

# ===========================
# """

#     enhanced_resume = f"{resume_text.strip()}\n\n{enhancement.strip()}"
#     logger.debug("Static resume optimization completed.")
#     logger.info(f"Added {len(unique_skills)} emphasized skills using fallback logic.")

#     summary = [
#         "Appended a skills justification section to the end of the resume.",
#         f"Included {len(unique_skills)} emphasized skills with user-provided context."
#     ]

#     return enhanced_resume, summary


# Optional: MVP legacy highlighting logic (not used in main flow)
def optimize_resume_for_job(resume_text: str, job_skills: List[str], emphasized_skills: List[str]) -> str:
    highlighted_resume = resume_text
    sorted_skills = sorted(set(job_skills), key=len, reverse=True)

    for skill in sorted_skills:
        if skill.lower() in resume_text.lower():
            replacement = f"**{skill.upper()}**" if skill in emphasized_skills else f"*{skill}*"
            highlighted_resume = re.sub(rf"\b{re.escape(skill)}\b", replacement, highlighted_resume, flags=re.IGNORECASE)

    return highlighted_resume
