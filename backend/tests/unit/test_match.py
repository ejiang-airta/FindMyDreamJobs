# File: backend/tests/unit/test_match.py

import pytest
from app.services.score_calc import calculate_match_score

def test_match_score_perfect_match():
    job_skills = {"python", "sql"}
    resume_text = "Proficient in Python development with years of SQL experience."
    job_description = "Looking for a proficient Python developer with years of SQL experience."

    result = calculate_match_score(resume_text, job_description, job_skills)
    print("Perfect test results: ",result)

    assert isinstance(result, float)
    assert result == 79.42
    # assert set(result["matched_skills"]) == {"python", "sql"}
    # assert result["missing_skills"] == []

def test_match_score_partial():
    job_skills = {"python", "sql", "aws"}
    resume_text = "Python developer with experience in SQL."
    job_description = "Looking for a Python developer with SQL experience. Familiarity with AWS is a plus."


    result = calculate_match_score(resume_text, job_description, job_skills)
    print("Partial test results: ",result)
    assert 0 < result < 100
    # assert "python" in result["matched_skills"]
    # assert "aws" in result["missing_skills"]
