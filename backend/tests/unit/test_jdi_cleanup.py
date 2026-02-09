# File: backend/tests/unit/test_jdi_cleanup.py
# Tests for JDI candidate retention and pruning
import pytest
from datetime import datetime, timezone, timedelta
from app.services.jdi.cleanup import prune_expired_candidates
from app.models.jdi_candidate import JDICandidate


class TestPruneExpiredCandidates:
    """Tests for JDI candidate pruning rules."""

    def test_prune_old_ignored_candidates(self, db_session, test_user):
        """Ignored candidates older than 14 days should be deleted."""
        old_date = datetime.now(timezone.utc) - timedelta(days=15)
        candidate = JDICandidate(
            user_id=test_user.id,
            source="linkedin",
            status="ignored",
            job_url_canonical="https://example.com/job/1",
            updated_at=old_date,
        )
        db_session.add(candidate)
        db_session.flush()

        result = prune_expired_candidates(db_session)
        assert result["ignored"] == 1

    def test_keep_recent_ignored_candidates(self, db_session, test_user):
        """Ignored candidates less than 14 days old should be kept."""
        recent_date = datetime.now(timezone.utc) - timedelta(days=5)
        candidate = JDICandidate(
            user_id=test_user.id,
            source="linkedin",
            status="ignored",
            job_url_canonical="https://example.com/job/2",
            updated_at=recent_date,
        )
        db_session.add(candidate)
        db_session.flush()

        result = prune_expired_candidates(db_session)
        assert result["ignored"] == 0

    def test_prune_old_promoted_candidates(self, db_session, test_user):
        """Promoted candidates older than 14 days should be deleted."""
        old_date = datetime.now(timezone.utc) - timedelta(days=15)
        candidate = JDICandidate(
            user_id=test_user.id,
            source="indeed",
            status="promoted",
            job_url_canonical="https://example.com/job/3",
            updated_at=old_date,
        )
        db_session.add(candidate)
        db_session.flush()

        result = prune_expired_candidates(db_session)
        assert result["promoted"] == 1

    def test_prune_stale_new_candidates(self, db_session, test_user):
        """New candidates older than 90 days should be deleted."""
        old_date = datetime.now(timezone.utc) - timedelta(days=91)
        candidate = JDICandidate(
            user_id=test_user.id,
            source="trueup",
            status="new",
            job_url_canonical="https://example.com/job/4",
            created_at=old_date,
        )
        db_session.add(candidate)
        db_session.flush()

        result = prune_expired_candidates(db_session)
        assert result["stale_new"] == 1

    def test_keep_recent_new_candidates(self, db_session, test_user):
        """New candidates less than 90 days old should be kept."""
        candidate = JDICandidate(
            user_id=test_user.id,
            source="trueup",
            status="new",
            job_url_canonical="https://example.com/job/5",
        )
        db_session.add(candidate)
        db_session.flush()

        result = prune_expired_candidates(db_session)
        assert result["stale_new"] == 0
