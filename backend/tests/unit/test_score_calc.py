"""Unit tests for app.services.score_calc -- ATS & match scoring engine."""

import pytest
from app.services.score_calc import (
    calculate_scores,
    calculate_similarity_score,
    calculate_keyword_score,
    calculate_skill_match_score,
    calculate_match_score,
    check_formatting_rules,
)

# ---------------------------------------------------------------------------
# Sample data
# ---------------------------------------------------------------------------

WELL_FORMATTED_RESUME = """
John Doe
john.doe@email.com | (555) 123-4567

Experience
Senior Software Engineer at Acme Corp
- Built microservices with Python, FastAPI, and PostgreSQL
- Led a team of 5 engineers to deliver a new product feature
- Improved CI/CD pipeline reducing deploy time by 40%

Education
B.Sc. Computer Science, University of Toronto

Skills
Python, JavaScript, TypeScript, AWS, Docker, Kubernetes, React, PostgreSQL
"""

PLAIN_TEXT_RESUME = "I am a developer and I know some stuff about coding."

JOB_DESCRIPTION = """
We are looking for a Senior Software Engineer with strong experience in
Python, FastAPI, PostgreSQL, Docker, and Kubernetes. Experience with AWS
and CI/CD pipelines is a plus. The role involves building microservices
and leading a small engineering team.
"""

JD_KEYWORDS = ["python", "fastapi", "postgresql", "docker", "kubernetes", "aws"]


# ---------------------------------------------------------------------------
# calculate_similarity_score
# ---------------------------------------------------------------------------

class TestSimilarityScore:
    def test_identical_texts_high_score(self):
        text = "Python FastAPI PostgreSQL Docker Kubernetes"
        score = calculate_similarity_score(text, text)
        assert score == 100.0

    def test_unrelated_texts_low_score(self):
        score = calculate_similarity_score(
            "Baking bread and pastries in a commercial kitchen",
            "Deploying Kubernetes clusters on AWS with Terraform",
        )
        assert score < 30

    def test_empty_job_description_returns_zero(self):
        score = calculate_similarity_score("Python developer resume", "")
        assert score == 0.0

    def test_returns_float(self):
        score = calculate_similarity_score("Python", "Python developer")
        assert isinstance(score, float)


# ---------------------------------------------------------------------------
# calculate_keyword_score
# ---------------------------------------------------------------------------

class TestKeywordScore:
    def test_all_keywords_present(self):
        text = "python javascript react aws docker kubernetes"
        keywords = ["python", "javascript", "react"]
        score = calculate_keyword_score(text, keywords)
        assert score > 0

    def test_no_keywords_present(self):
        text = "baking bread pastry cooking"
        keywords = ["python", "javascript", "react"]
        score = calculate_keyword_score(text, keywords)
        assert score == 0

    def test_partial_keywords(self):
        text = "python and react developer"
        keywords = ["python", "javascript", "react", "aws"]
        score = calculate_keyword_score(text, keywords)
        assert score > 0


# ---------------------------------------------------------------------------
# calculate_skill_match_score
# ---------------------------------------------------------------------------

class TestSkillMatchScore:
    def test_full_match(self):
        resume = "python fastapi postgresql docker kubernetes aws"
        score = calculate_skill_match_score(resume, JD_KEYWORDS)
        assert score == 100.0

    def test_partial_match(self):
        resume = "python fastapi"
        score = calculate_skill_match_score(resume, JD_KEYWORDS)
        assert 0 < score < 100

    def test_no_match(self):
        resume = "baking pastry cooking"
        score = calculate_skill_match_score(resume, JD_KEYWORDS)
        assert score == 0.0

    def test_empty_keywords_returns_zero(self):
        score = calculate_skill_match_score("python developer", [])
        assert score == 0.0


# ---------------------------------------------------------------------------
# calculate_match_score
# ---------------------------------------------------------------------------

class TestMatchScore:
    def test_returns_float_in_range(self):
        score = calculate_match_score(
            WELL_FORMATTED_RESUME, JOB_DESCRIPTION, JD_KEYWORDS
        )
        assert isinstance(score, float)
        assert 0 <= score <= 100

    def test_high_overlap_produces_higher_score(self):
        high = calculate_match_score(
            "python fastapi postgresql docker kubernetes aws", JOB_DESCRIPTION, JD_KEYWORDS
        )
        low = calculate_match_score(
            "baking pastry cooking bread", JOB_DESCRIPTION, JD_KEYWORDS
        )
        assert high > low


# ---------------------------------------------------------------------------
# check_formatting_rules
# ---------------------------------------------------------------------------

class TestFormattingRules:
    def test_with_email_no_warning(self):
        warnings = check_formatting_rules(WELL_FORMATTED_RESUME)
        assert not any("email" in w.lower() for w in warnings)

    def test_without_email_warns(self):
        warnings = check_formatting_rules("No contact info here at all. " * 50)
        assert any("email" in w.lower() for w in warnings)

    def test_with_experience_keyword(self):
        warnings = check_formatting_rules(WELL_FORMATTED_RESUME)
        assert not any("experience" in w.lower() and "keyword" in w.lower() for w in warnings)

    def test_short_resume_warns(self):
        warnings = check_formatting_rules("Short.")
        assert any("short" in w.lower() for w in warnings)

    def test_long_resume_warns(self):
        warnings = check_formatting_rules("word " * 5000)
        assert any("long" in w.lower() for w in warnings)


# ---------------------------------------------------------------------------
# calculate_scores (unified entry point)
# ---------------------------------------------------------------------------

class TestCalculateScores:
    def test_returns_tuple_of_three(self):
        result = calculate_scores(WELL_FORMATTED_RESUME, JOB_DESCRIPTION, JD_KEYWORDS)
        assert isinstance(result, tuple)
        assert len(result) == 3

    def test_ats_score_is_float(self):
        ats, _, _ = calculate_scores(WELL_FORMATTED_RESUME)
        assert isinstance(ats, float)

    def test_ats_score_capped_at_85(self):
        ats, _, _ = calculate_scores(WELL_FORMATTED_RESUME)
        assert ats <= 85

    def test_empty_resume_returns_zeros(self):
        ats, match, warnings = calculate_scores("")
        assert ats == 0.0
        assert match == 0.0
        assert len(warnings) > 0

    def test_match_score_nonzero_with_jd(self):
        _, match, _ = calculate_scores(WELL_FORMATTED_RESUME, JOB_DESCRIPTION, JD_KEYWORDS)
        assert match > 0

    def test_match_score_zero_without_jd(self):
        _, match, _ = calculate_scores(WELL_FORMATTED_RESUME)
        assert match == 0.0
