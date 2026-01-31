"""API tests for resume download endpoint."""

import pytest
from app.models.resume import Resume
from datetime import datetime, timezone


class TestDownloadOptimizedResume:
    def test_not_found(self, client):
        resp = client.get("/download-optimized-resume/999999")
        assert resp.status_code == 404

    def test_not_optimized(self, client, test_resume):
        """Resume without optimized_text should return 400."""
        # test_resume fixture has no optimized_text
        resp = client.get(f"/download-optimized-resume/{test_resume.id}")
        assert resp.status_code == 400

    def test_success(self, client, db_session, test_user):
        """Resume with optimized_text should return a .docx file."""
        resume = Resume(
            user_id=test_user.id,
            resume_name="optimized_test.txt",
            file_path="uploads/resumes/optimized_test.txt",
            parsed_text="Original resume text",
            optimized_text=(
                "John Doe\njohn@email.com\n\n"
                "Experience\nSenior Engineer at Acme Corp\n"
                "- Built microservices with Python\n\n"
                "Skills\nPython, AWS, Docker"
            ),
            is_user_approved=True,
            created_at=datetime.now(timezone.utc),
        )
        db_session.add(resume)
        db_session.flush()

        resp = client.get(f"/download-optimized-resume/{resume.id}")
        assert resp.status_code == 200
        assert "application/vnd.openxmlformats" in resp.headers.get("content-type", "")
