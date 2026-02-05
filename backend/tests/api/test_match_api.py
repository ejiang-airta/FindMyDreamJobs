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


class TestQuickMatchScore:
    def test_success(self, client, test_user, test_resume):
        """Test quick match score calculation for search results."""
        res = client.post("/quick-match-score", json={
            "user_id": test_user.id,
            "job_description": "Python developer with 5 years experience"
        })
        assert res.status_code == 200
        data = res.json()
        assert "match_score" in data
        assert isinstance(data["match_score"], (int, float))
        assert 0 <= data["match_score"] <= 100
        assert "resume_used" in data

    def test_no_resume(self, client, db_session):
        """Test quick match when user has no resume."""
        from app.models.user import User
        # Create a user without a resume
        new_user = User(
            email="no_resume@test.com",
            full_name="No Resume",
            hashed_password="dummy"
        )
        db_session.add(new_user)
        db_session.commit()
        db_session.refresh(new_user)

        res = client.post("/quick-match-score", json={
            "user_id": new_user.id,
            "job_description": "Python developer"
        })
        assert res.status_code == 200
        data = res.json()
        assert data["match_score"] == 0
        assert "No resume found" in data["message"]
