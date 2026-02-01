"""API tests for match scoring endpoints."""

import pytest


class TestCalculateMatchScore:
    def test_success(self, client, test_user, test_resume, test_job):
        resp = client.post("/match-score", json={
            "resume_id": test_resume.id,
            "job_id": test_job.id,
        })
        assert resp.status_code == 200
        data = resp.json()
        assert "match_score" in data
        assert "ats_score" in data
        assert "matched_skills" in data
        assert "missing_skills" in data
        assert isinstance(data["match_score"], (int, float))

    def test_missing_resume(self, client, test_job):
        resp = client.post("/match-score", json={
            "resume_id": 999999,
            "job_id": test_job.id,
        })
        assert resp.status_code == 404

    def test_missing_job(self, client, test_resume):
        resp = client.post("/match-score", json={
            "resume_id": test_resume.id,
            "job_id": 999999,
        })
        assert resp.status_code == 404


class TestGetMatches:
    def test_get_all_matches(self, client, test_match):
        resp = client.get("/matches")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)
        assert len(data) >= 1

    def test_get_matches_by_user(self, client, test_user, test_match):
        resp = client.get(f"/matches/{test_user.id}")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)
        assert len(data) >= 1
