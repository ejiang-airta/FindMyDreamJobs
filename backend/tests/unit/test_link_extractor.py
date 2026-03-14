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

    def test_linkedin_comm_normalized_to_jobs(self):
        """LinkedIn /comm/jobs/view/ID and /jobs/view/ID should produce the same canonical URL."""
        url_comm = "https://www.linkedin.com/comm/jobs/view/4186041345?refId=abc&trackingId=xyz"
        url_direct = "https://www.linkedin.com/jobs/view/4186041345?refId=def&trackingId=pqr"
        assert normalize_url(url_comm) == normalize_url(url_direct)

    def test_linkedin_comm_strip_tracking(self):
        url = "https://www.linkedin.com/comm/jobs/view/123?refId=abc&trackingId=xyz"
        normalized = normalize_url(url)
        assert "/comm/" not in normalized
        assert "refId" not in normalized
        assert "trackingId" not in normalized
        assert "123" in normalized


class TestIndeedUrlPatterns:
    """New Indeed URL patterns cover current jobalert.indeed.com sender links."""

    def test_jobalert_indeed_redirect_matched(self):
        """donotreply@jobalert.indeed.com emails link through jobalert.indeed.com."""
        html = '<a href="https://r.jobalert.indeed.com/rdr?jk=abc123">Director of Technology</a>'
        links = extract_job_links(html, "indeed")
        assert len(links) == 1
        assert "jobalert.indeed.com" in links[0]

    def test_r_indeed_redirect_matched(self):
        html = '<a href="https://r.indeed.com/rdr?job=qa-manager&jk=xyz789">QA Manager</a>'
        links = extract_job_links(html, "indeed")
        assert len(links) == 1

    def test_click_indeed_matched(self):
        html = '<a href="https://click.indeed.com/track?jk=abc&tt=1">Engineering Director</a>'
        links = extract_job_links(html, "indeed")
        assert len(links) == 1

    def test_indeed_unsubscribe_still_excluded(self):
        """Even with broader patterns, unsubscribe links must be filtered."""
        html = """
        <a href="https://r.jobalert.indeed.com/rdr?jk=abc">Director Role</a>
        <a href="https://r.jobalert.indeed.com/unsubscribe?token=xyz">Unsubscribe</a>
        """
        links = extract_job_links(html, "indeed")
        assert len(links) == 1
        assert "unsubscribe" not in links[0]

    def test_multiple_indeed_jobs_extracted(self):
        """Indeed emails with 3 jobs per alert should extract all 3."""
        html = """
        <a href="https://r.jobalert.indeed.com/rdr?jk=aaa">Director of Technology & AI Enablement</a>
        <a href="https://r.jobalert.indeed.com/rdr?jk=bbb">Quality Assurance Manager</a>
        <a href="https://r.jobalert.indeed.com/rdr?jk=ccc">VP of Engineering</a>
        """
        links = extract_job_links(html, "indeed")
        assert len(links) == 3


class TestTrueUpUrlPatterns:
    """TrueUp URL patterns cover direct job pages and email tracking subdomains."""

    def test_trueup_direct_job_link(self):
        html = '<a href="https://trueup.io/jobs/director-engineering-docebo-54321">Director, Engineering</a>'
        links = extract_job_links(html, "trueup")
        assert len(links) == 1

    def test_trueup_app_subdomain(self):
        html = '<a href="https://app.trueup.io/jobs/vp-engineering-123">VP Engineering</a>'
        links = extract_job_links(html, "trueup")
        assert len(links) == 1

    def test_trueup_click_tracking(self):
        """TrueUp email campaigns may use click.trueup.io tracking URLs."""
        html = '<a href="https://click.trueup.io/ls/click?upn=abc123">Director of Software Development</a>'
        links = extract_job_links(html, "trueup")
        assert len(links) == 1

    def test_trueup_links_subdomain(self):
        html = '<a href="https://links.trueup.io/u/abc?jid=456">Principal Engineer</a>'
        links = extract_job_links(html, "trueup")
        assert len(links) == 1

    def test_trueup_unsubscribe_still_excluded(self):
        html = """
        <a href="https://trueup.io/jobs/director-eng-123">Director of Engineering</a>
        <a href="https://trueup.io/unsubscribe?token=abc">Unsubscribe</a>
        """
        links = extract_job_links(html, "trueup")
        assert len(links) == 1
        assert "unsubscribe" not in links[0]

    def test_trueup_7_jobs_per_digest(self):
        """TrueUp digest sends 7 jobs per week — all should be extracted."""
        jobs = "\n".join(
            f'<a href="https://trueup.io/jobs/job-{i}-slug">Job {i} Title Here</a>'
            for i in range(1, 8)
        )
        html = f"<html><body>{jobs}</body></html>"
        links = extract_job_links(html, "trueup")
        assert len(links) == 7


class TestLinkedInShortener:
    """lnkd.in shortener URLs used in some LinkedIn email campaigns."""

    def test_lnkd_in_matched(self):
        html = '<a href="https://lnkd.in/eABCDEFG">Quality Assurance Manager</a>'
        links = extract_job_links(html, "linkedin")
        assert len(links) == 1
        assert "lnkd.in" in links[0]
