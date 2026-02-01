"""API tests for ATS scoring endpoint."""

import pytest


class TestATSScore:
    def test_success(self, client, test_resume):
        """ATS score endpoint should return 200 with scoring data."""
        resp = client.post("/ats-score", params={"resume_id": test_resume.id})
        assert resp.status_code == 200
        data = resp.json()
        assert "ats_score_initial" in data
        assert isinstance(data["ats_score_initial"], (int, float))
        assert "ats_score_final" in data
        assert "warnings" in data
        assert isinstance(data["warnings"], list)
        assert data["message"] == "ATS Score stored successfully."

    def test_not_found(self, client):
        resp = client.post("/ats-score", params={"resume_id": 999999})
        assert resp.status_code == 404
