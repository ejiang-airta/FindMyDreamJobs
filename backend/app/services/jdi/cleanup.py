# File: backend/app/services/jdi/cleanup.py
# Retention and pruning for JDI candidates
import logging
from datetime import datetime, timezone, timedelta
from sqlalchemy.orm import Session

from app.models.jdi_candidate import JDICandidate

logger = logging.getLogger(__name__)


def prune_expired_candidates(db: Session) -> dict:
    """
    Clean up expired JDI candidates based on retention rules:

    - status=ignored AND updated_at < 14 days ago → DELETE
    - status=promoted AND updated_at < 14 days ago → DELETE
    - status=new AND created_at < 90 days ago → DELETE (safety cap)

    Returns:
        Dict with counts of deleted candidates per category.
    """
    now = datetime.now(timezone.utc)
    results = {"ignored": 0, "promoted": 0, "stale_new": 0}

    # Prune ignored candidates (14 days)
    cutoff_14d = now - timedelta(days=14)

    ignored_count = (
        db.query(JDICandidate)
        .filter(
            JDICandidate.status == "ignored",
            JDICandidate.updated_at < cutoff_14d,
        )
        .delete(synchronize_session="fetch")
    )
    results["ignored"] = ignored_count

    # Prune promoted candidates (14 days)
    promoted_count = (
        db.query(JDICandidate)
        .filter(
            JDICandidate.status == "promoted",
            JDICandidate.updated_at < cutoff_14d,
        )
        .delete(synchronize_session="fetch")
    )
    results["promoted"] = promoted_count

    # Prune stale new candidates (90 days safety cap)
    cutoff_90d = now - timedelta(days=90)

    stale_count = (
        db.query(JDICandidate)
        .filter(
            JDICandidate.status == "new",
            JDICandidate.created_at < cutoff_90d,
        )
        .delete(synchronize_session="fetch")
    )
    results["stale_new"] = stale_count

    db.commit()

    total = sum(results.values())
    if total > 0:
        logger.info(f"Pruned {total} JDI candidates: {results}")

    return results
