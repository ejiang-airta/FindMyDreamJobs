"""API tests for resume endpoints."""

import io
import os
import pytest


class TestUploadResume:
    def test_upload_txt(self, client, test_user):
        content = b"John Doe\njohn@email.com\nExperience\nSenior Engineer at Acme\nSkills: Python, AWS"
        resp = client.post(
            "/upload-resume",
            data={"user_id": str(test_user.id)},
            files={"file": ("test_resume.txt", io.BytesIO(content), "text/plain")},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert "resume_id" in data
        assert data["resume_id"] > 0

        # Cleanup uploaded file
        if "file_path" in data and os.path.exists(data["file_path"]):
            os.remove(data["file_path"])

    def test_upload_duplicate_name(self, client, test_user):
        content = b"Resume content"
        # First upload
        resp1 = client.post(
            "/upload-resume",
            data={"user_id": str(test_user.id), "resume_name": "dup_test.txt"},
            files={"file": ("dup_test.txt", io.BytesIO(content), "text/plain")},
        )
        # Cleanup first file
        if resp1.status_code == 200 and "file_path" in resp1.json():
            fp = resp1.json()["file_path"]
            if os.path.exists(fp):
                os.remove(fp)

        # Second upload with same name
        resp2 = client.post(
            "/upload-resume",
            data={"user_id": str(test_user.id), "resume_name": "dup_test.txt"},
            files={"file": ("dup_test.txt", io.BytesIO(content), "text/plain")},
        )
        assert resp2.status_code == 200
        data = resp2.json()
        assert data.get("status") == "duplicate"


class TestGetResumes:
    def test_get_resumes_by_user(self, client, test_user, test_resume):
        resp = client.get(f"/resumes/by-user/{test_user.id}")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert data[0]["user_id"] == test_user.id

    def test_get_resume_by_id(self, client, test_resume):
        resp = client.get(f"/resumes/{test_resume.id}")
        assert resp.status_code == 200
        data = resp.json()
        assert data["id"] == test_resume.id
        assert "parsed_text" in data

    def test_get_resume_not_found(self, client):
        resp = client.get("/resumes/999999")
        assert resp.status_code == 404

    def test_get_all_resumes(self, client, test_resume):
        resp = client.get("/resumes")
        assert resp.status_code == 200
        assert isinstance(resp.json(), list)
