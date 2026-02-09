# File: backend/tests/unit/test_jd_fetcher.py
# Tests for JD text extraction and cleaning
import pytest
from app.services.jdi.jd_fetcher import extract_jd_text, clean_jd_text, compute_jd_hash


class TestExtractJdText:
    """Tests for source-aware JD extraction from HTML."""

    def test_linkedin_selector(self):
        html = """
        <html><body>
            <div class="description__text">
                <p>We are looking for a Senior Software Engineer with Python experience.
                You will build microservices and lead a team of developers.
                Requirements: 5+ years experience, AWS, Docker, Kubernetes.
                Nice to have: Machine Learning background.</p>
            </div>
        </body></html>
        """
        text, confidence = extract_jd_text(html, "linkedin")
        assert text is not None
        assert confidence >= 90
        assert "Senior Software Engineer" in text

    def test_indeed_selector(self):
        html = """
        <html><body>
            <div id="jobDescriptionText">
                <p>Full-stack developer needed for a fast-paced startup.
                Must have experience with React, Node.js, PostgreSQL.
                We offer competitive salary, remote work, and great benefits.</p>
            </div>
        </body></html>
        """
        text, confidence = extract_jd_text(html, "indeed")
        assert text is not None
        assert confidence >= 90
        assert "React" in text

    def test_generic_fallback(self):
        html = """
        <html><body>
            <div class="job-description">
                <p>Backend Developer position at TechCorp.
                We need someone with Python and Django experience.
                Competitive compensation and flexible schedule provided.</p>
            </div>
        </body></html>
        """
        text, confidence = extract_jd_text(html, "other")
        assert text is not None
        assert confidence >= 60

    def test_no_jd_found(self):
        html = "<html><body><p>Hello</p></body></html>"
        text, confidence = extract_jd_text(html, "other")
        # Either None or very low confidence
        assert confidence < 60 or text is None

    def test_empty_html(self):
        text, confidence = extract_jd_text("", "linkedin")
        assert confidence == 0


class TestCleanJdText:
    """Tests for JD text cleaning."""

    def test_collapses_whitespace(self):
        text = "Senior   Software    Engineer"
        cleaned = clean_jd_text(text)
        assert "  " not in cleaned

    def test_strips_blank_lines(self):
        text = "Line 1\n\n\n\nLine 2"
        cleaned = clean_jd_text(text)
        assert "\n\n\n" not in cleaned

    def test_handles_empty_input(self):
        assert clean_jd_text("") == ""
        assert clean_jd_text(None) == ""


class TestComputeJdHash:
    """Tests for JD hash computation."""

    def test_same_text_same_hash(self):
        text = "This is a job description"
        assert compute_jd_hash(text) == compute_jd_hash(text)

    def test_different_text_different_hash(self):
        assert compute_jd_hash("Text A") != compute_jd_hash("Text B")

    def test_returns_64_char_hex(self):
        h = compute_jd_hash("test")
        assert len(h) == 64
        assert all(c in "0123456789abcdef" for c in h)
