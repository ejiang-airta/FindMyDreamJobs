# File: backend/tests/api/test_profile_api.py
# API integration tests for JDI user profile/preferences
import pytest
from app.models.user_profile import UserProfile


class TestGetProfile:
    """Tests for GET /api/profile/{user_id}."""

    def test_profile_not_found(self, client, test_user):
        """404 when no profile exists."""
        res = client.get(f"/api/profile/{test_user.id}")
        assert res.status_code == 404

    def test_get_existing_profile(self, client, test_user, db_session):
        """Get profile that was previously created."""
        profile = UserProfile(
            user_id=test_user.id,
            target_titles=["Software Engineer"],
            jdi_min_score=70,
            jdi_sources_enabled=["linkedin", "indeed"],
        )
        db_session.add(profile)
        db_session.flush()

        res = client.get(f"/api/profile/{test_user.id}")
        assert res.status_code == 200
        data = res.json()
        assert data["user_id"] == test_user.id
        assert data["target_titles"] == ["Software Engineer"]
        assert data["jdi_min_score"] == 70
        assert data["jdi_sources_enabled"] == ["linkedin", "indeed"]


class TestUpdateProfile:
    """Tests for PUT /api/profile/{user_id}."""

    def test_create_profile(self, client, test_user):
        """PUT creates a new profile if none exists (upsert)."""
        res = client.put(
            f"/api/profile/{test_user.id}",
            json={
                "target_titles": ["Data Engineer", "Backend Developer"],
                "jdi_min_score": 75,
                "jdi_sources_enabled": ["linkedin"],
            },
        )
        assert res.status_code == 200
        data = res.json()
        assert data["user_id"] == test_user.id
        assert data["target_titles"] == ["Data Engineer", "Backend Developer"]
        assert data["jdi_min_score"] == 75

    def test_update_existing_profile(self, client, test_user, db_session):
        """PUT updates existing profile with only provided fields."""
        profile = UserProfile(
            user_id=test_user.id,
            target_titles=["Engineer"],
            jdi_min_score=60,
        )
        db_session.add(profile)
        db_session.flush()

        # Update only min_score
        res = client.put(
            f"/api/profile/{test_user.id}",
            json={"jdi_min_score": 80},
        )
        assert res.status_code == 200
        data = res.json()
        assert data["jdi_min_score"] == 80
        # Original field preserved
        assert data["target_titles"] == ["Engineer"]

    def test_update_nonexistent_user(self, client):
        """PUT fails for user that doesn't exist."""
        res = client.put(
            "/api/profile/99999",
            json={"jdi_min_score": 50},
        )
        assert res.status_code == 404

    def test_update_resume_select_mode(self, client, test_user):
        """Can set resume selection mode."""
        res = client.put(
            f"/api/profile/{test_user.id}",
            json={"jdi_resume_select_mode": "keyword_rules"},
        )
        assert res.status_code == 200
        assert res.json()["jdi_resume_select_mode"] == "keyword_rules"

    def test_invalid_resume_select_mode(self, client, test_user):
        """Invalid resume_select_mode is rejected."""
        res = client.put(
            f"/api/profile/{test_user.id}",
            json={"jdi_resume_select_mode": "invalid_mode"},
        )
        assert res.status_code == 422
