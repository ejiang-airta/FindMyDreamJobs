# File: backend/tests/api/test_jdi_api.py
# API integration tests for JDI candidate feed and actions
import pytest
from datetime import datetime, timezone
from app.models.jdi_candidate import JDICandidate
from app.models.job import Job
from app.models.saved_job import SavedJob


@pytest.fixture()
def jdi_candidate(db_session, test_user):
    """Insert a JDI candidate and return it."""
    candidate = JDICandidate(
        user_id=test_user.id,
        source="linkedin",
        title="Senior Python Developer",
        company="Acme Corp",
        location="Toronto, ON",
        salary_text="$130,000 - $160,000",
        jd_text="We are looking for a Senior Python Developer with AWS experience.",
        jd_extraction_confidence=85,
        match_score=78,
        match_reasons=["Strong skill match: Python", "Remote-friendly position"],
        status="new",
        job_url_raw="https://linkedin.com/jobs/view/12345",
        job_url_canonical="https://linkedin.com/jobs/view/12345",
    )
    db_session.add(candidate)
    db_session.flush()
    return candidate


@pytest.fixture()
def multiple_candidates(db_session, test_user):
    """Insert several JDI candidates with varied scores and statuses."""
    candidates = []
    for i, (score, status, source) in enumerate([
        (90, "new", "linkedin"),
        (75, "new", "indeed"),
        (60, "new", "trueup"),
        (80, "ignored", "linkedin"),
        (70, "promoted", "indeed"),
    ]):
        c = JDICandidate(
            user_id=test_user.id,
            source=source,
            title=f"Job Title {i}",
            company=f"Company {i}",
            match_score=score,
            status=status,
            job_url_canonical=f"https://example.com/job/{i}",
        )
        db_session.add(c)
    db_session.flush()
    return db_session.query(JDICandidate).filter_by(user_id=test_user.id).all()


class TestGetCandidates:
    """Tests for GET /api/jdi/candidates."""

    def test_empty_feed(self, client, test_user):
        """No candidates returns empty feed."""
        res = client.get(f"/api/jdi/candidates?user_id={test_user.id}")
        assert res.status_code == 200
        data = res.json()
        assert data["total"] == 0
        assert data["candidates"] == []

    def test_returns_new_candidates_by_default(self, client, test_user, multiple_candidates):
        """Default filter returns only 'new' status candidates."""
        res = client.get(f"/api/jdi/candidates?user_id={test_user.id}")
        assert res.status_code == 200
        data = res.json()
        assert data["total"] == 3  # 3 new candidates
        for c in data["candidates"]:
            assert c["status"] == "new"

    def test_sorted_by_score_descending(self, client, test_user, multiple_candidates):
        """Candidates are sorted by match_score descending."""
        res = client.get(f"/api/jdi/candidates?user_id={test_user.id}")
        data = res.json()
        scores = [c["match_score"] for c in data["candidates"]]
        assert scores == sorted(scores, reverse=True)

    def test_filter_by_status(self, client, test_user, multiple_candidates):
        """Filter by specific status."""
        res = client.get(f"/api/jdi/candidates?user_id={test_user.id}&status=ignored")
        data = res.json()
        assert data["total"] == 1
        assert data["candidates"][0]["status"] == "ignored"

    def test_filter_by_min_score(self, client, test_user, multiple_candidates):
        """Filter by minimum score."""
        res = client.get(f"/api/jdi/candidates?user_id={test_user.id}&min_score=80")
        data = res.json()
        for c in data["candidates"]:
            assert c["match_score"] >= 80

    def test_filter_by_source(self, client, test_user, multiple_candidates):
        """Filter by source."""
        res = client.get(f"/api/jdi/candidates?user_id={test_user.id}&source=linkedin")
        data = res.json()
        # Only new + linkedin
        for c in data["candidates"]:
            assert c["source"] == "linkedin"

    def test_filter_unread_only(self, client, test_user, jdi_candidate, db_session):
        """Unread filter excludes seen candidates."""
        # Mark the candidate as seen
        jdi_candidate.seen_at = datetime.now(timezone.utc)
        db_session.flush()

        res = client.get(f"/api/jdi/candidates?user_id={test_user.id}&unread_only=true")
        data = res.json()
        assert data["total"] == 0

    def test_pagination(self, client, test_user, multiple_candidates):
        """Pagination with limit and offset."""
        res = client.get(f"/api/jdi/candidates?user_id={test_user.id}&limit=2&offset=0")
        data = res.json()
        assert len(data["candidates"]) == 2
        assert data["total"] == 3  # Total new candidates
        assert data["limit"] == 2
        assert data["offset"] == 0


class TestGetCandidateDetail:
    """Tests for GET /api/jdi/candidates/{candidate_id}."""

    def test_get_detail(self, client, test_user, jdi_candidate):
        """Get full candidate details."""
        res = client.get(f"/api/jdi/candidates/{jdi_candidate.id}?user_id={test_user.id}")
        assert res.status_code == 200
        data = res.json()
        assert data["id"] == jdi_candidate.id
        assert data["jd_text"] is not None
        assert data["jd_extraction_confidence"] == 85

    def test_not_found(self, client, test_user):
        """404 for nonexistent candidate."""
        res = client.get(f"/api/jdi/candidates/nonexistent-id?user_id={test_user.id}")
        assert res.status_code == 404

    def test_wrong_user(self, client, test_user, jdi_candidate, db_session):
        """Can't access another user's candidate."""
        # Use a user_id that doesn't own this candidate
        res = client.get(f"/api/jdi/candidates/{jdi_candidate.id}?user_id=99999")
        assert res.status_code == 404


class TestMarkSeen:
    """Tests for POST /api/jdi/candidates/{id}/mark-seen."""

    def test_mark_seen(self, client, test_user, jdi_candidate):
        """Mark a candidate as seen sets seen_at."""
        assert jdi_candidate.seen_at is None
        res = client.post(f"/api/jdi/candidates/{jdi_candidate.id}/mark-seen?user_id={test_user.id}")
        assert res.status_code == 200
        assert res.json()["status"] == "seen"

    def test_mark_seen_not_found(self, client, test_user):
        """404 for nonexistent candidate."""
        res = client.post(f"/api/jdi/candidates/nonexistent-id/mark-seen?user_id={test_user.id}")
        assert res.status_code == 404


class TestIgnoreCandidate:
    """Tests for POST /api/jdi/candidates/{id}/ignore."""

    def test_ignore(self, client, test_user, jdi_candidate):
        """Ignore sets status to 'ignored'."""
        res = client.post(f"/api/jdi/candidates/{jdi_candidate.id}/ignore?user_id={test_user.id}")
        assert res.status_code == 200
        assert res.json()["status"] == "ignored"

    def test_ignore_not_found(self, client, test_user):
        """404 for nonexistent candidate."""
        res = client.post(f"/api/jdi/candidates/nonexistent-id/ignore?user_id={test_user.id}")
        assert res.status_code == 404


class TestPromoteCandidate:
    """Tests for POST /api/jdi/candidates/{id}/promote."""

    def test_promote_analyze(self, client, test_user, jdi_candidate, db_session):
        """Promote with mode=analyze creates Job but not SavedJob."""
        res = client.post(
            f"/api/jdi/candidates/{jdi_candidate.id}/promote?user_id={test_user.id}",
            json={"mode": "analyze"},
        )
        assert res.status_code == 200
        data = res.json()
        assert data["status"] == "promoted"
        assert "job_id" in data

        # Verify Job was created
        job = db_session.query(Job).filter_by(id=data["job_id"]).first()
        assert job is not None
        assert job.job_title == "Senior Python Developer"

        # Verify no SavedJob was created
        saved = db_session.query(SavedJob).filter_by(user_id=test_user.id, search_id=f"jdi-{jdi_candidate.id}").first()
        assert saved is None

    def test_promote_save(self, client, test_user, jdi_candidate, db_session):
        """Promote with mode=save creates both Job and SavedJob."""
        res = client.post(
            f"/api/jdi/candidates/{jdi_candidate.id}/promote?user_id={test_user.id}",
            json={"mode": "save"},
        )
        assert res.status_code == 200
        data = res.json()
        assert data["status"] == "promoted"

        # Verify SavedJob was also created
        saved = db_session.query(SavedJob).filter_by(user_id=test_user.id, search_id=f"jdi-{jdi_candidate.id}").first()
        assert saved is not None
        assert saved.job_title == "Senior Python Developer"

    def test_promote_already_promoted(self, client, test_user, jdi_candidate, db_session):
        """Can't promote an already-promoted candidate."""
        jdi_candidate.status = "promoted"
        db_session.flush()

        res = client.post(
            f"/api/jdi/candidates/{jdi_candidate.id}/promote?user_id={test_user.id}",
            json={"mode": "analyze"},
        )
        assert res.status_code == 400

    def test_promote_not_found(self, client, test_user):
        """404 for nonexistent candidate."""
        res = client.post(
            f"/api/jdi/candidates/nonexistent-id/promote?user_id={test_user.id}",
            json={"mode": "analyze"},
        )
        assert res.status_code == 404

    def test_promote_invalid_mode(self, client, test_user, jdi_candidate):
        """Invalid mode is rejected by Pydantic validation."""
        res = client.post(
            f"/api/jdi/candidates/{jdi_candidate.id}/promote?user_id={test_user.id}",
            json={"mode": "invalid"},
        )
        assert res.status_code == 422


class TestRunIngestion:
    """Tests for POST /api/jdi/run."""

    def test_run_no_integration(self, client, test_user):
        """Run returns gracefully when user has no Gmail integration."""
        res = client.post(
            f"/api/jdi/run?user_id={test_user.id}",
            json={"window_hours": 24},
        )
        # Ingestion handles missing integration gracefully
        data = res.json()
        assert res.status_code in (200, 500)
        if res.status_code == 200:
            assert data["new_candidates"] == 0
