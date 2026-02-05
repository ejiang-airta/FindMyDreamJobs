# File: backend/tests/unit/test_jdi_scoring.py
# Tests for JDI resume selection and scoring
import pytest
from unittest.mock import MagicMock, patch
from app.services.jdi.scoring import select_best_resume, _apply_keyword_rules


class TestSelectBestResume:
    """Tests for auto_best resume selection."""

    def test_no_resumes_returns_none(self):
        db = MagicMock()
        db.query.return_value.filter_by.return_value.first.return_value = None
        db.query.return_value.filter.return_value.order_by.return_value.limit.return_value.all.return_value = []

        resume_id, score = select_best_resume(user_id=1, jd_text="Python developer needed", db=db)
        assert resume_id is None
        assert score == 0

    def test_empty_jd_returns_none(self):
        db = MagicMock()
        resume_id, score = select_best_resume(user_id=1, jd_text="", db=db)
        assert resume_id is None
        assert score == 0

    def test_blank_jd_returns_none(self):
        db = MagicMock()
        resume_id, score = select_best_resume(user_id=1, jd_text="   ", db=db)
        assert resume_id is None
        assert score == 0


class TestApplyKeywordRules:
    """Tests for keyword-based resume selection rules."""

    def test_matching_rule(self):
        rules = {"python": 1, "java": 2}
        resume1 = MagicMock()
        resume1.id = 1
        resume2 = MagicMock()
        resume2.id = 2

        result = _apply_keyword_rules("Looking for a Python developer", rules, [resume1, resume2])
        assert result == 1

    def test_no_matching_rule(self):
        rules = {"python": 1}
        resume1 = MagicMock()
        resume1.id = 1

        result = _apply_keyword_rules("Looking for a Go developer", rules, [resume1])
        assert result is None

    def test_first_rule_wins(self):
        rules = {"python": 1, "developer": 2}
        resume1 = MagicMock()
        resume1.id = 1
        resume2 = MagicMock()
        resume2.id = 2

        result = _apply_keyword_rules("Python developer needed", rules, [resume1, resume2])
        assert result == 1  # "python" matches first

    def test_rule_with_invalid_resume_id(self):
        rules = {"python": 99}  # Resume 99 doesn't exist
        resume1 = MagicMock()
        resume1.id = 1

        result = _apply_keyword_rules("Python developer", rules, [resume1])
        assert result is None  # 99 not in available resumes
