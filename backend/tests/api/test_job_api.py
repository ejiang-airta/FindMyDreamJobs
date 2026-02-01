"""API tests for job endpoints (parse, analyze, CRUD, save/unsave)."""

import pytest


SAMPLE_JD = """
Senior Software Engineer

About Tech Corp
Tech Corp is a leading technology company based in Toronto, ON.

We are looking for a Senior Software Engineer with 5+ years of experience in
Python, FastAPI, PostgreSQL, Docker, and Kubernetes. Experience with AWS
and CI/CD pipelines is a plus.

Salary: $140,000 - $180,000 per year

Requirements:
- 5+ years of experience in software development
- Strong knowledge of Python and FastAPI
- Experience with PostgreSQL and Docker
"""


class TestParseJobDescription:
    def test_parse_success(self, client, test_user):
        resp = client.post("/parse-job-description", json={
            "user_id": test_user.id,
            "job_description": SAMPLE_JD,
        })
        assert resp.status_code == 200
        data = resp.json()
        assert "job_id" in data
        assert data["job_id"] > 0
        assert "skills" in data

    def test_parse_missing_input(self, client, test_user):
        resp = client.post("/parse-job-description", json={
            "user_id": test_user.id,
            # no job_description or job_link
        })
        assert resp.status_code == 400


class TestAnalyzeSearchedJob:
    def test_analyze_success(self, client, test_user):
        resp = client.post("/analyze-searched-job", json={
            "user_id": test_user.id,
            "job_title": "Data Scientist",
            "employer_name": "DataCo",
            "job_description": "Looking for a data scientist with Python and SQL skills.",
            "job_location": "Vancouver, BC",
        })
        assert resp.status_code == 200

    def test_analyze_missing_required_field(self, client, test_user):
        resp = client.post("/analyze-searched-job", json={
            "user_id": test_user.id,
            "job_title": "Engineer",
            # missing employer_name and job_description
        })
        assert resp.status_code == 400


class TestJobCRUD:
    def test_get_jobs_by_user(self, client, test_user, test_job):
        resp = client.get(f"/jobs/by-user/{test_user.id}")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)
        assert len(data) >= 1

    def test_get_job_by_id(self, client, test_job):
        resp = client.get(f"/jobs/{test_job.id}")
        assert resp.status_code == 200
        data = resp.json()
        assert data["job_id"] == test_job.id
        assert data["job_title"] == "Senior Software Engineer"

    def test_get_job_not_found(self, client):
        resp = client.get("/jobs/999999")
        assert resp.status_code == 404

    def test_update_job(self, client, test_job):
        resp = client.put(f"/jobs/{test_job.id}", json={
            "salary": "$150,000 - $200,000",
            "location": "Remote",
        })
        assert resp.status_code == 200

    def test_get_jobs_by_user_empty(self, client, test_user):
        # Use a user_id that has no jobs
        resp = client.get("/jobs/by-user/999999")
        assert resp.status_code == 404


class TestSaveUnsaveJob:
    def test_save_job(self, client, test_user):
        resp = client.post("/save-job", json={
            "user_id": test_user.id,
            "job": {
                "job_id": "search-abc-123",
                "job_title": "ML Engineer",
                "employer_name": "AI Corp",
                "employer_logo": None,
                "employer_website": "https://aicorp.com",
                "job_location": "Remote",
                "job_is_remote": True,
                "job_employment_type": "Full-time",
                "job_salary": "$120K - $160K",
                "job_description": "Build ML pipelines with Python and TensorFlow.",
                "job_google_link": "https://google.com/jobs/123",
                "job_posted_at_datetime_utc": "2025-01-15T10:00:00Z",
            },
        })
        assert resp.status_code == 200
        assert "saved" in resp.json()["message"].lower() or "already" in resp.json()["message"].lower()

    def test_save_job_duplicate(self, client, test_user):
        payload = {
            "user_id": test_user.id,
            "job": {
                "job_id": "dup-search-456",
                "job_title": "Backend Dev",
                "employer_name": "DevCo",
                "job_location": "Toronto",
                "job_google_link": "https://google.com/jobs/456",
                "job_posted_at_datetime_utc": "2025-01-15T10:00:00Z",
                "employer_logo": None,
                "employer_website": None,
                "job_is_remote": False,
                "job_employment_type": "Full-time",
                "job_salary": None,
                "job_description": "Backend developer role.",
            },
        }
        # First save
        client.post("/save-job", json=payload)
        # Second save (duplicate)
        resp2 = client.post("/save-job", json=payload)
        assert resp2.status_code == 200
        assert "already" in resp2.json()["message"].lower()

    def test_unsave_job(self, client, test_user):
        # Save first
        client.post("/save-job", json={
            "user_id": test_user.id,
            "job": {
                "job_id": "unsave-test-789",
                "job_title": "DevOps",
                "employer_name": "OpsCo",
                "job_location": "Remote",
                "job_google_link": "https://google.com/jobs/789",
                "job_posted_at_datetime_utc": "2025-01-15T10:00:00Z",
                "employer_logo": None,
                "employer_website": None,
                "job_is_remote": True,
                "job_employment_type": "Full-time",
                "job_salary": None,
                "job_description": "DevOps role.",
            },
        })
        # Unsave
        resp = client.post("/unsave-job", json={
            "user_id": test_user.id,
            "search_id": "unsave-test-789",
        })
        assert resp.status_code == 200

    def test_get_saved_jobs(self, client, test_user):
        resp = client.get(f"/saved-jobs/{test_user.id}")
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)
