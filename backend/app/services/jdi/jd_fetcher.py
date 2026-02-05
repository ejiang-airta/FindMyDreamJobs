# File: backend/app/services/jdi/jd_fetcher.py
# Fetch and extract job description text from job posting URLs
import hashlib
import logging
import re
from typing import Optional
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

# Browser-like headers for fetching job pages
REQUEST_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}

# Source-specific CSS selectors for JD extraction
SOURCE_SELECTORS = {
    "linkedin": [
        ".description__text",
        ".show-more-less-html__markup",
        ".jobs-description__content",
        "[class*='description']",
    ],
    "indeed": [
        "#jobDescriptionText",
        ".jobsearch-jobDescriptionText",
        "[id*='jobDescription']",
    ],
    "trueup": [
        ".job-description",
        "[class*='description']",
    ],
}


def fetch_jd_html(url: str, timeout: int = 15) -> Optional[str]:
    """
    Fetch the HTML content of a job posting page.

    Args:
        url: The canonical job URL.
        timeout: Request timeout in seconds.

    Returns:
        Raw HTML string or None on failure.
    """
    try:
        resp = requests.get(url, headers=REQUEST_HEADERS, timeout=timeout)
        resp.raise_for_status()
        return resp.text
    except requests.RequestException as e:
        logger.warning(f"Failed to fetch JD from {url[:80]}: {e}")
        return None


def _extract_with_selectors(soup: BeautifulSoup, source: str) -> Optional[str]:
    """Try source-specific CSS selectors to find the JD."""
    selectors = SOURCE_SELECTORS.get(source, [])
    for selector in selectors:
        el = soup.select_one(selector)
        if el:
            text = el.get_text(separator="\n", strip=True)
            if len(text) > 100:  # Minimum viable JD length
                return text
    return None


def _extract_with_trafilatura(html: str) -> Optional[str]:
    """Fallback extraction using trafilatura if available."""
    try:
        import trafilatura
        text = trafilatura.extract(html, include_comments=False, include_tables=True)
        return text if text and len(text) > 100 else None
    except ImportError:
        logger.debug("trafilatura not installed, skipping fallback extraction")
        return None


def _extract_generic(soup: BeautifulSoup) -> Optional[str]:
    """
    Generic fallback: look for the largest text block that looks like a JD.
    Searches for common JD container patterns.
    """
    # Common class/id patterns for job descriptions
    patterns = [
        re.compile(r"job.?desc", re.IGNORECASE),
        re.compile(r"description", re.IGNORECASE),
        re.compile(r"posting.?body", re.IGNORECASE),
        re.compile(r"job.?detail", re.IGNORECASE),
    ]

    candidates = []
    for pattern in patterns:
        # Search by class name
        elements = soup.find_all(class_=pattern)
        for el in elements:
            text = el.get_text(separator="\n", strip=True)
            if len(text) > 100:
                candidates.append(text)

        # Search by id
        elements = soup.find_all(id=pattern)
        for el in elements:
            text = el.get_text(separator="\n", strip=True)
            if len(text) > 100:
                candidates.append(text)

    if candidates:
        # Return the longest candidate
        return max(candidates, key=len)

    return None


def extract_jd_text(html: str, source: str = "other") -> tuple[Optional[str], int]:
    """
    Extract job description text from HTML using source-aware strategies.

    Args:
        html: Raw HTML of the job posting page.
        source: Source name (linkedin, indeed, trueup, other).

    Returns:
        Tuple of (jd_text, extraction_confidence 0-100).
        - confidence 90+: source-specific selector matched
        - confidence 60-89: generic pattern or trafilatura
        - confidence 0: extraction failed
    """
    soup = BeautifulSoup(html, "html.parser")

    # Strategy 1: Source-specific selectors
    text = _extract_with_selectors(soup, source)
    if text:
        cleaned = clean_jd_text(text)
        return cleaned, 90

    # Strategy 2: Generic CSS pattern matching
    text = _extract_generic(soup)
    if text:
        cleaned = clean_jd_text(text)
        return cleaned, 70

    # Strategy 3: trafilatura fallback
    text = _extract_with_trafilatura(html)
    if text:
        cleaned = clean_jd_text(text)
        return cleaned, 60

    # Strategy 4: Last resort — get all body text
    body = soup.find("body")
    if body:
        text = body.get_text(separator="\n", strip=True)
        if len(text) > 200:
            # Truncate to ~5000 chars max (likely contains boilerplate)
            cleaned = clean_jd_text(text[:5000])
            return cleaned, 30

    return None, 0


def clean_jd_text(raw_text: str) -> str:
    """
    Clean extracted JD text:
    - Normalize whitespace
    - Remove excessive blank lines
    - Strip boilerplate markers
    - Remove job aggregator marketing content
    """
    if not raw_text:
        return ""

    # Strip marketing content from job aggregators (recruit.net, etc.)
    # Look for patterns that indicate where actual job content starts
    job_content_markers = [
        "ABOUT ", "About ", "The Company", "The Role", "Position:",
        "Job Description:", "Company:", "Overview:", "The Opportunity",
    ]

    # Find the earliest marker position
    earliest_marker_pos = len(raw_text)
    for marker in job_content_markers:
        pos = raw_text.find(marker)
        if pos != -1 and pos < earliest_marker_pos and pos < 1000:
            # Only use markers in first 1000 chars (where junk appears)
            earliest_marker_pos = pos

    # If we found a marker, trim everything before it
    if earliest_marker_pos < len(raw_text) and earliest_marker_pos > 0:
        raw_text = raw_text[earliest_marker_pos:]

    # Remove common navigation/footer elements that pollute extraction
    nav_junk_lines = [
        "Gain full access to exclusive job listings",
        "Verified, High-Quality Jobs Only",
        "No ads, scams, or junk",
        "Focus on Real Opportunities",
        "Exclusive Resume Review",
        "Receive expert feedback with personalized suggestions",
        "Go Premium",
        "Your shortcut to unlisted jobs",
        "Cover letters that get noticed",
        "ATS-proof, tailored, AI-powered",
        "Match you with headhunters",
        "Home Jobs Headhunters Resume",
        "There are open tasks for you",
        "Quick links",
        "Important links related to your searches",
        "New job search",
        "Previous job searches",
        "Advantage 01", "Advantage 02", "Advantage 03", "Advantage 04",
        "Every job. One platform",
        "Win more interviews",
        "Craft a standout resume",
        # Generic job site navigation
        "Sign in", "Sign up", "Create account",
        "Upload your resume", "Post a job",
    ]

    # Normalize whitespace within lines
    lines = raw_text.split("\n")
    cleaned_lines = []
    for line in lines:
        line = line.strip()
        if line:
            # Collapse multiple spaces
            line = re.sub(r"\s+", " ", line)
            # Skip navigation/junk lines
            if any(junk.lower() in line.lower() for junk in nav_junk_lines):
                continue
            # Skip very short lines that are likely nav items (1-3 chars)
            if len(line) <= 3 and not any(c.isalnum() for c in line):
                continue
            cleaned_lines.append(line)

    # Remove excessive blank lines (max 1 consecutive blank)
    result_lines = []
    prev_blank = False
    for line in cleaned_lines:
        if not line:
            if not prev_blank:
                result_lines.append("")
            prev_blank = True
        else:
            result_lines.append(line)
            prev_blank = False

    return "\n".join(result_lines).strip()


def compute_jd_hash(jd_text: str) -> str:
    """Compute SHA-256 hash of JD text for quick deduplication."""
    return hashlib.sha256(jd_text.encode("utf-8")).hexdigest()
