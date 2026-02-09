# File: backend/app/services/jdi/link_extractor.py
# Extract and canonicalize job posting URLs from email HTML
import re
import logging
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse, unquote
from bs4 import BeautifulSoup
import requests

logger = logging.getLogger(__name__)

# URL patterns that indicate a job posting (not unsubscribe, settings, etc.)
JOB_URL_PATTERNS = {
    "linkedin": [
        re.compile(r"linkedin\.com/jobs/view/\d+", re.IGNORECASE),
        re.compile(r"linkedin\.com/comm/jobs/view/\d+", re.IGNORECASE),
    ],
    "indeed": [
        re.compile(r"indeed\.com/viewjob", re.IGNORECASE),
        re.compile(r"indeed\.com/rc/clk", re.IGNORECASE),
    ],
    "trueup": [
        re.compile(r"trueup\.io/job/", re.IGNORECASE),
        re.compile(r"trueup\.io/jobs/", re.IGNORECASE),
    ],
}

# URL patterns to EXCLUDE (unsubscribe, settings, social links)
EXCLUDE_PATTERNS = [
    re.compile(r"unsubscribe", re.IGNORECASE),
    re.compile(r"email-preferences", re.IGNORECASE),
    re.compile(r"notifications/settings", re.IGNORECASE),
    re.compile(r"help\.linkedin\.com", re.IGNORECASE),
    re.compile(r"privacy", re.IGNORECASE),
    re.compile(r"terms", re.IGNORECASE),
]

# Tracking parameters to strip during normalization
TRACKING_PARAMS = {
    "utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content",
    "refid", "trackingid", "trk", "midtoken", "midsig", "ebp",
    "rcposting", "original_referer", "tk", "advn",
}


def extract_job_links(html_body: str, source: str = "other") -> list[str]:
    """
    Parse email HTML and extract job posting URLs.

    Args:
        html_body: Raw HTML email body.
        source: Source name (linkedin, indeed, trueup, other).

    Returns:
        List of raw job URLs (before canonicalization).
    """
    if not html_body:
        return []

    soup = BeautifulSoup(html_body, "html.parser")
    all_links = set()

    for tag in soup.find_all("a", href=True):
        href = tag["href"].strip()
        if not href or href.startswith("mailto:"):
            continue

        # Skip excluded patterns
        if any(pattern.search(href) for pattern in EXCLUDE_PATTERNS):
            continue

        # Check if URL matches known job patterns for this source
        source_patterns = JOB_URL_PATTERNS.get(source, [])
        if source_patterns:
            if any(p.search(href) for p in source_patterns):
                all_links.add(href)
        else:
            # For unknown sources, include any http(s) link that looks job-related
            if re.search(r"(job|career|position|apply|opening)", href, re.IGNORECASE):
                all_links.add(href)

    logger.debug(f"Extracted {len(all_links)} job links from {source} email")
    return list(all_links)


def resolve_canonical_url(raw_url: str, timeout: int = 10) -> str:
    """
    Follow redirects to resolve the final canonical URL.
    LinkedIn and Indeed emails often use tracking redirect URLs.

    Args:
        raw_url: The original URL from the email.
        timeout: Request timeout in seconds.

    Returns:
        The final resolved URL after redirects.
    """
    if "linkedin.com" in (raw_url or ""):
        # LinkedIn redirects often lead to auth/login pages, destroying the real target
        return raw_url
    try:
        resp = requests.head(
            raw_url,
            allow_redirects=True,
            timeout=timeout,
            headers={"User-Agent": "Mozilla/5.0 (compatible; JobBot/1.0)"},
        )
        final_url = resp.url
        logger.debug(f"Resolved: {raw_url[:80]} → {final_url[:80]}")
        return final_url
    except requests.RequestException as e:
        logger.warning(f"Failed to resolve URL {raw_url[:80]}: {e}")
        return raw_url  # Fall back to original URL


def normalize_url(url: str) -> str:
    """
    Normalize a job URL for deduplication:
    1. Strip tracking parameters
    2. Remove fragments
    3. Lowercase the scheme and host
    4. Decode percent-encoded characters

    Args:
        url: The URL to normalize.

    Returns:
        A canonical URL string suitable as a deduplication key.
    """
    url = unquote(url)
    parsed = urlparse(url)

    # Lowercase scheme and host
    scheme = parsed.scheme.lower()
    netloc = parsed.netloc.lower()

    # Strip tracking params from query string
    query_params = parse_qs(parsed.query, keep_blank_values=False)
    cleaned_params = {
        k: v for k, v in query_params.items()
        if k.lower() not in TRACKING_PARAMS
    }
    # Sort params for consistent ordering
    clean_query = urlencode(cleaned_params, doseq=True) if cleaned_params else ""

    # Remove fragment
    canonical = urlunparse((scheme, netloc, parsed.path, parsed.params, clean_query, ""))

    # Remove trailing slash for consistency
    canonical = canonical.rstrip("/")

    return canonical
