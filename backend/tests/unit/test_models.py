"""Unit tests for SQLAlchemy models -- field existence and defaults."""

import pytest
from app.models.user import User
from app.models.resume import Resume
from app.models.job import Job
from app.models.application import Application
from app.models.match import JobMatch
from app.models.saved_job import SavedJob


class TestUserModel:
    def test_has_expected_columns(self):
        cols = {c.name for c in User.__table__.columns}
        expected = {"id", "full_name", "email", "hashed_password", "created_at", "updated_at", "wizard_progress"}
        assert expected.issubset(cols)

    def test_tablename(self):
        assert User.__tablename__ == "users"


class TestResumeModel:
    def test_has_expected_columns(self):
        cols = {c.name for c in Resume.__table__.columns}
        expected = {
            "id", "user_id", "resume_name", "file_path", "parsed_text",
            "optimized_text", "is_ai_generated", "is_user_approved",
            "ats_score_initial", "ats_score_final", "created_at", "updated_at",
        }
        assert expected.issubset(cols)

    def test_defaults(self):
        r = Resume.__table__.columns
        assert r["is_ai_generated"].default.arg is False
        assert r["is_user_approved"].default.arg is False


class TestJobModel:
    def test_has_extracted_skills_jsonb(self):
        cols = {c.name for c in Job.__table__.columns}
        assert "extracted_skills" in cols

    def test_has_salary_field(self):
        cols = {c.name for c in Job.__table__.columns}
        assert "salary" in cols

    def test_tablename(self):
        assert Job.__tablename__ == "jobs"


class TestApplicationModel:
    def test_has_status_field(self):
        cols = {c.name for c in Application.__table__.columns}
        assert "application_status" in cols

    def test_has_foreign_keys(self):
        cols = {c.name for c in Application.__table__.columns}
        assert {"user_id", "job_id", "resume_id"}.issubset(cols)


class TestJobMatchModel:
    def test_has_score_fields(self):
        cols = {c.name for c in JobMatch.__table__.columns}
        assert {"match_score_initial", "match_score_final", "ats_score_initial", "ats_score_final"}.issubset(cols)

    def test_has_skills_text_fields(self):
        cols = {c.name for c in JobMatch.__table__.columns}
        assert {"matched_skills", "missing_skills"}.issubset(cols)


class TestSavedJobModel:
    def test_has_search_id(self):
        cols = {c.name for c in SavedJob.__table__.columns}
        assert "search_id" in cols

    def test_has_job_fields(self):
        cols = {c.name for c in SavedJob.__table__.columns}
        expected = {"job_title", "employer_name", "job_location", "job_apply_link"}
        assert expected.issubset(cols)

    def test_tablename(self):
        assert SavedJob.__tablename__ == "saved_jobs"
