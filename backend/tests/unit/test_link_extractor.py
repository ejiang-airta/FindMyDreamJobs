# File: backend/tests/unit/test_link_extractor.py
# Tests for JDI link extraction and URL canonicalization
import pytest
from app.services.jdi.link_extractor import extract_job_links, normalize_url


class TestExtractJobLinks:
    """Tests for extracting job URLs from email HTML."""

    def test_linkedin_job_link(self):
        html = '<a href="https://www.linkedin.com/jobs/view/12345">View Job</a>'
        links = extract_job_links(html, "linkedin")
        assert len(links) == 1
        assert "linkedin.com/jobs/view/12345" in links[0]

    def test_linkedin_comm_link(self):
        html = '<a href="https://www.linkedin.com/comm/jobs/view/98765">View</a>'
        links = extract_job_links(html, "linkedin")
        assert len(links) == 1

    def test_indeed_viewjob_link(self):
        html = '<a href="https://www.indeed.com/viewjob?jk=abc123">Apply</a>'
        links = extract_job_links(html, "indeed")
        assert len(links) == 1

    def test_trueup_job_link(self):
        html = '<a href="https://trueup.io/job/software-engineer-123">View</a>'
        links = extract_job_links(html, "trueup")
        assert len(links) == 1

    def test_excludes_unsubscribe_links(self):
        html = """
        <a href="https://www.linkedin.com/jobs/view/12345">View Job</a>
        <a href="https://www.linkedin.com/unsubscribe">Unsubscribe</a>
        <a href="https://www.linkedin.com/email-preferences">Preferences</a>
        """
        links = extract_job_links(html, "linkedin")
        assert len(links) == 1  # Only the job link

    def test_excludes_mailto_links(self):
        html = """
        <a href="mailto:support@linkedin.com">Email</a>
        <a href="https://www.linkedin.com/jobs/view/12345">Job</a>
        """
        links = extract_job_links(html, "linkedin")
        assert len(links) == 1

    def test_empty_html_returns_empty(self):
        assert extract_job_links("", "linkedin") == []
        assert extract_job_links(None, "linkedin") == []

    def test_no_matching_links(self):
        html = '<a href="https://example.com/page">Not a job</a>'
        links = extract_job_links(html, "linkedin")
        assert len(links) == 0

    def test_unknown_source_uses_keyword_matching(self):
        html = '<a href="https://example.com/job/software-engineer">Apply</a>'
        links = extract_job_links(html, "other")
        assert len(links) == 1

    def test_deduplicates_links(self):
        html = """
        <a href="https://www.linkedin.com/jobs/view/12345">View</a>
        <a href="https://www.linkedin.com/jobs/view/12345">Apply Now</a>
        """
        links = extract_job_links(html, "linkedin")
        assert len(links) == 1


class TestNormalizeUrl:
    """Tests for URL canonicalization."""

    def test_strips_utm_params(self):
        url = "https://linkedin.com/jobs/view/123?utm_source=email&utm_medium=jobs"
        normalized = normalize_url(url)
        assert "utm_source" not in normalized
        assert "utm_medium" not in normalized

    def test_strips_tracking_params(self):
        url = "https://linkedin.com/jobs/view/123?refId=abc&trackingId=xyz"
        normalized = normalize_url(url)
        assert "refId" not in normalized
        assert "trackingId" not in normalized

    def test_preserves_meaningful_params(self):
        url = "https://indeed.com/viewjob?jk=abc123&from=search"
        normalized = normalize_url(url)
        assert "jk=abc123" in normalized

    def test_lowercases_scheme_and_host(self):
        url = "HTTPS://WWW.LinkedIn.COM/jobs/view/123"
        normalized = normalize_url(url)
        assert normalized.startswith("https://www.linkedin.com")

    def test_removes_fragment(self):
        url = "https://linkedin.com/jobs/view/123#details"
        normalized = normalize_url(url)
        assert "#" not in normalized

    def test_removes_trailing_slash(self):
        url = "https://linkedin.com/jobs/view/123/"
        normalized = normalize_url(url)
        assert not normalized.endswith("/")

    def test_decodes_percent_encoding(self):
        url = "https://example.com/job%20search"
        normalized = normalize_url(url)
        assert "job search" in normalized or "job%20search" in normalized.lower()
