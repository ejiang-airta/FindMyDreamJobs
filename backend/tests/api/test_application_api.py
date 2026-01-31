"""API tests for application endpoints."""

import pytest


class TestSubmitApplication:
    def test_success(self, client, test_user, test_resume, test_job):
        resp = client.post("/submit-application", json={
            "resume_id": test_resume.id,
            "job_id": test_job.id,
            "application_url": "https://techcorp.com/apply/123",
        })
        assert resp.status_code == 200
        data = resp.json()
        assert "application_id" in data
        assert "application recorded successfully" in data["status"].lower()

    def test_bad_resume_id(self, client, test_job):
        resp = client.post("/submit-application", json={
            "resume_id": 999999,
            "job_id": test_job.id,
        })
        assert resp.status_code == 404

    def test_bad_job_id(self, client, test_resume):
        resp = client.post("/submit-application", json={
            "resume_id": test_resume.id,
            "job_id": 999999,
        })
        assert resp.status_code == 404


class TestGetApplications:
    def test_get_user_applications(self, client, test_user, test_resume, test_job):
        # Submit one first
        client.post("/submit-application", json={
            "resume_id": test_resume.id,
            "job_id": test_job.id,
        })
        resp = client.get(f"/applications/{test_user.id}")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)
        assert len(data) >= 1

    def test_empty_applications(self, client):
        # User with no applications
        resp = client.get("/applications/999999")
        assert resp.status_code == 200
        assert resp.json() == []


class TestUpdateApplicationStatus:
    def test_update_status(self, client, test_user, test_resume, test_job):
        # Submit first
        submit_resp = client.post("/submit-application", json={
            "resume_id": test_resume.id,
            "job_id": test_job.id,
        })
        app_id = submit_resp.json()["application_id"]

        # Update status
        resp = client.put(
            "/update-application-status",
            params={"application_id": app_id, "status": "Interview Scheduled"},
        )
        assert resp.status_code == 200

    def test_update_nonexistent(self, client):
        resp = client.put(
            "/update-application-status",
            params={"application_id": 999999, "status": "Rejected"},
        )
        assert resp.status_code == 404
