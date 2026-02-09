# File: backend/tests/unit/test_gmail_scanner.py
# Tests for Gmail search query construction
import pytest
from app.services.jdi.gmail_scanner import build_search_query, _get_message_body_html
import base64


class TestBuildSearchQuery:
    """Tests for Gmail search query construction."""

    def test_all_sources_default(self):
        query = build_search_query(sources=None, window_hours=24)
        assert "jobs-noreply@linkedin.com" in query
        assert "alert@indeed.com" in query
        assert "trueup.io" in query
        assert "newer_than:1d" in query

    def test_single_source(self):
        query = build_search_query(sources=["linkedin"], window_hours=24)
        assert "jobs-noreply@linkedin.com" in query
        assert "indeed.com" not in query
        assert "trueup.io" not in query

    def test_multiple_sources(self):
        query = build_search_query(sources=["linkedin", "indeed"], window_hours=24)
        assert "jobs-noreply@linkedin.com" in query
        assert "alert@indeed.com" in query
        assert "trueup.io" not in query

    def test_window_hours_1_day(self):
        query = build_search_query(window_hours=24)
        assert "newer_than:1d" in query

    def test_window_hours_3_days(self):
        query = build_search_query(window_hours=72)
        assert "newer_than:3d" in query

    def test_window_hours_7_days(self):
        query = build_search_query(window_hours=168)
        assert "newer_than:7d" in query

    def test_unknown_source_returns_empty(self):
        query = build_search_query(sources=["nonexistent"])
        assert query == ""

    def test_from_clause_uses_or(self):
        query = build_search_query(sources=["linkedin", "indeed"])
        assert " OR " in query


class TestGetMessageBodyHtml:
    """Tests for extracting HTML body from Gmail payload."""

    def test_simple_html_body(self):
        encoded = base64.urlsafe_b64encode(b"<p>Hello World</p>").decode()
        payload = {"mimeType": "text/html", "body": {"data": encoded}}
        result = _get_message_body_html(payload)
        assert "Hello World" in result

    def test_multipart_with_html(self):
        encoded = base64.urlsafe_b64encode(b"<p>Job Alert</p>").decode()
        payload = {
            "mimeType": "multipart/alternative",
            "parts": [
                {"mimeType": "text/plain", "body": {"data": base64.urlsafe_b64encode(b"plain text").decode()}},
                {"mimeType": "text/html", "body": {"data": encoded}},
            ],
        }
        result = _get_message_body_html(payload)
        assert "Job Alert" in result

    def test_empty_payload(self):
        result = _get_message_body_html({})
        assert result == ""

    def test_fallback_to_plain_text(self):
        encoded = base64.urlsafe_b64encode(b"Plain text content").decode()
        payload = {
            "mimeType": "multipart/alternative",
            "parts": [
                {"mimeType": "text/plain", "body": {"data": encoded}},
            ],
        }
        result = _get_message_body_html(payload)
        assert "Plain text content" in result
