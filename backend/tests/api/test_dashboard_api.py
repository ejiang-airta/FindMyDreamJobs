"""API tests for wizard/dashboard progress endpoints."""

import pytest


class TestWizardProgress:
    def test_update_progress(self, client, test_user):
        resp = client.post("/wizard/progress", json={
            "email": test_user.email,
            "step": "analyze",
        })
        assert resp.status_code == 200
        assert resp.json()["step"] == "analyze"

    def test_get_progress(self, client, test_user):
        # Set progress first
        client.post("/wizard/progress", json={
            "email": test_user.email,
            "step": "match",
        })
        # Read it back
        resp = client.post("/wizard/progress/get", json={
            "email": test_user.email,
        })
        assert resp.status_code == 200
        assert resp.json()["step"] == "match"

    def test_get_default_progress(self, client, test_user):
        """New user with no wizard_progress should default to 'upload'."""
        resp = client.post("/wizard/progress/get", json={
            "email": test_user.email,
        })
        assert resp.status_code == 200
        # wizard_progress is None for a fresh user -> defaults to "upload"
        step = resp.json()["step"]
        assert step is not None

    def test_update_missing_email(self, client):
        resp = client.post("/wizard/progress", json={"step": "analyze"})
        assert resp.status_code == 400

    def test_update_missing_step(self, client, test_user):
        resp = client.post("/wizard/progress", json={"email": test_user.email})
        assert resp.status_code == 400

    def test_get_progress_nonexistent_user(self, client):
        resp = client.post("/wizard/progress/get", json={
            "email": "nobody@example.com",
        })
        assert resp.status_code == 404
