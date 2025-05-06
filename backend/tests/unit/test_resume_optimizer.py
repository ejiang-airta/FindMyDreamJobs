# File: backend/tests/unit/test_resume_optimizer.py

import pytest
from typing import Tuple, List
from app.services.resume_optimizer import optimize_resume_with_skills_service

def test_optimize_resume_basic():
    resume_text = "Experienced software developer with expertise in Python and cloud platforms. Python backend development experience in a cloud platform i.e. AWS/GCP/Azure."
    emphasized_skills = {"python", "cloud"}
    justification = "These are critical for the job."

    result = optimize_resume_with_skills_service(
        resume_text=resume_text,
        matched_skills ={"python","cloud"},
        missing_skills = {"aws", "gcp", "azure"},
        emphasized_skills=emphasized_skills,
        justification=justification
    )
    print("optimize test results: ",result)

    assert isinstance(result, tuple)
    assert "Python" in result[0] or "python" in result[0]
    assert "cloud" in result[0]
    assert "backend development" in result[0]
