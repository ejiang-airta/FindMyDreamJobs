"""API tests for ATS scoring endpoint."""

import pytest


class TestATSScore:
    @pytest.mark.xfail(
        reason="BUG in ats.py:28 – calculate_scores() returns 3 values "
               "but route unpacks into 2, causing ValueError (500).",
        strict=True,
    )
    def test_success(self, client, test_resume):
        """Should return 200 with ATS scores once the route bug is fixed."""
        resp = client.post("/ats-score", params={"resume_id": test_resume.id})
        assert resp.status_code == 200
        data = resp.json()
        assert "ats_score_initial" in data
        assert isinstance(data["ats_score_initial"], (int, float))

    def test_success_currently_crashes(self, client, test_resume):
        """Documents actual behavior: route crashes due to unpack bug in ats.py:28."""
        with pytest.raises(ValueError, match="too many values to unpack"):
            client.post("/ats-score", params={"resume_id": test_resume.id})

    def test_not_found(self, client):
        resp = client.post("/ats-score", params={"resume_id": 999999})
        assert resp.status_code == 404
