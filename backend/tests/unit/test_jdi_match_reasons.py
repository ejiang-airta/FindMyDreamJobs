# File: backend/tests/unit/test_jdi_match_reasons.py
# Tests for match reason bullet generation
import pytest
from app.services.jdi.match_reasons import generate_match_reasons


class TestGenerateMatchReasons:
    """Tests for deterministic match reason generation."""

    def test_returns_list_of_strings(self):
        reasons = generate_match_reasons(
            resume_text="Python developer with AWS experience",
            jd_text="Looking for a Python developer with AWS and Docker skills",
            match_score=75,
        )
        assert isinstance(reasons, list)
        assert all(isinstance(r, str) for r in reasons)

    def test_returns_at_least_2_reasons(self):
        reasons = generate_match_reasons(
            resume_text="Software engineer",
            jd_text="Software engineer needed",
            match_score=50,
        )
        assert len(reasons) >= 2

    def test_returns_at_most_4_reasons(self):
        reasons = generate_match_reasons(
            resume_text="Senior Python AWS Docker Kubernetes DevOps cloud infrastructure engineer with fintech healthcare experience remote",
            jd_text="Senior Python AWS Docker Kubernetes DevOps cloud infrastructure engineer for fintech company offering remote work",
            match_score=95,
        )
        assert len(reasons) <= 4

    def test_skill_overlap_detection(self):
        reasons = generate_match_reasons(
            resume_text="Expert in Python, JavaScript, and React with 5 years of experience",
            jd_text="We need a developer skilled in Python and React for our frontend team",
            match_score=80,
        )
        # Should mention skills
        reasons_text = " ".join(reasons).lower()
        assert "skill" in reasons_text or "python" in reasons_text or "react" in reasons_text

    def test_remote_detection(self):
        reasons = generate_match_reasons(
            resume_text="Software engineer looking for remote work",
            jd_text="This is a fully remote position for a backend developer",
            match_score=70,
            jd_location="Remote",
        )
        reasons_text = " ".join(reasons).lower()
        assert "remote" in reasons_text

    def test_empty_inputs(self):
        reasons = generate_match_reasons(
            resume_text="",
            jd_text="",
            match_score=0,
        )
        assert len(reasons) >= 1  # Should still return at least a fallback

    def test_high_score_gets_positive_fallback(self):
        reasons = generate_match_reasons(
            resume_text="Generic text without keywords",
            jd_text="Another generic text",
            match_score=75,
        )
        reasons_text = " ".join(reasons).lower()
        # High score should get positive language
        assert "strong" in reasons_text or "alignment" in reasons_text or "relevant" in reasons_text
