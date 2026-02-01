# File: backend/tests/unit/test_resume_optimizer.py

import pytest
from unittest.mock import patch, MagicMock
from typing import Tuple, List
from app.services.resume_optimizer import optimize_resume_with_skills_service


def _make_mock_response(content: str):
    """Build a mock OpenAI ChatCompletion response."""
    choice = MagicMock()
    choice.message.content = content
    response = MagicMock()
    response.choices = [choice]
    return response


FAKE_GPT_RESPONSE = """===========================
Optimized Resume:
Experienced Python software developer with deep expertise in Python backend development
and cloud platforms (AWS, GCP, Azure). Proven track record in building scalable cloud-native
applications. Strong background in backend development using Python frameworks.

Changes Summary:
- Emphasized Python expertise throughout the resume
- Highlighted cloud platform experience with specific provider names
- Improved ATS-friendly keyword density for backend development
==========================="""


class TestOptimizeResumeWithSkills:
    @patch("app.services.resume_optimizer.client")
    def test_basic_optimization(self, mock_client):
        """Test that GPT response is correctly parsed into (text, changes) tuple."""
        mock_client.chat.completions.create.return_value = _make_mock_response(FAKE_GPT_RESPONSE)

        result = optimize_resume_with_skills_service(
            resume_text="Experienced software developer with expertise in Python and cloud platforms.",
            matched_skills={"python", "cloud"},
            missing_skills={"aws", "gcp", "azure"},
            emphasized_skills={"python", "cloud"},
            justification="These are critical for the job."
        )

        assert isinstance(result, tuple)
        assert len(result) == 2
        optimized_text, changes = result
        assert "Python" in optimized_text or "python" in optimized_text
        assert "cloud" in optimized_text
        assert isinstance(changes, list)
        assert len(changes) >= 1

    @patch("app.services.resume_optimizer.client")
    def test_gpt_called_with_correct_model(self, mock_client):
        """Verify we call GPT-4o with the correct params."""
        mock_client.chat.completions.create.return_value = _make_mock_response(FAKE_GPT_RESPONSE)

        optimize_resume_with_skills_service(
            resume_text="Some resume text.",
            matched_skills={"python"},
            missing_skills=set(),
            emphasized_skills={"python"},
            justification="Important skill."
        )

        call_kwargs = mock_client.chat.completions.create.call_args
        assert call_kwargs.kwargs["model"] == "gpt-4o"
        assert call_kwargs.kwargs["temperature"] == 0.7

    @patch("app.services.resume_optimizer.client")
    def test_missing_skills_filtered_by_justification(self, mock_client):
        """Only missing skills mentioned in the justification should be included in the prompt."""
        mock_client.chat.completions.create.return_value = _make_mock_response(FAKE_GPT_RESPONSE)

        optimize_resume_with_skills_service(
            resume_text="Resume text here.",
            matched_skills={"python"},
            missing_skills={"aws", "docker", "kubernetes"},
            emphasized_skills={"python"},
            justification="I have extensive AWS experience from my previous role."
        )

        call_kwargs = mock_client.chat.completions.create.call_args
        prompt = call_kwargs.kwargs["messages"][1]["content"]
        # "aws" is in the justification, so it should appear as allowed
        assert "aws" in prompt.lower()

    @patch("app.services.resume_optimizer.client")
    def test_changes_summary_parsed(self, mock_client):
        """Verify changes summary bullet points are correctly extracted."""
        mock_client.chat.completions.create.return_value = _make_mock_response(FAKE_GPT_RESPONSE)

        _, changes = optimize_resume_with_skills_service(
            resume_text="Resume text.",
            matched_skills={"python"},
            missing_skills=set(),
            emphasized_skills={"python"},
            justification="Important."
        )

        assert isinstance(changes, list)
        assert len(changes) == 3
        assert any("Python" in c for c in changes)

    @patch("app.services.resume_optimizer.client")
    def test_malformed_gpt_response_raises(self, mock_client):
        """If GPT returns no 'Optimized Resume:' section, a ValueError is raised."""
        mock_client.chat.completions.create.return_value = _make_mock_response(
            "Here is some random text without the expected format."
        )

        with pytest.raises(ValueError, match="GPT did not return a valid optimized resume"):
            optimize_resume_with_skills_service(
                resume_text="Resume text.",
                matched_skills=set(),
                missing_skills=set(),
                emphasized_skills=set(),
                justification=""
            )

    @patch("app.services.resume_optimizer.client")
    def test_api_error_propagates(self, mock_client):
        """If OpenAI API raises an exception, it propagates up."""
        mock_client.chat.completions.create.side_effect = Exception("API rate limit exceeded")

        with pytest.raises(Exception, match="API rate limit exceeded"):
            optimize_resume_with_skills_service(
                resume_text="Resume text.",
                matched_skills=set(),
                missing_skills=set(),
                emphasized_skills=set(),
                justification=""
            )
