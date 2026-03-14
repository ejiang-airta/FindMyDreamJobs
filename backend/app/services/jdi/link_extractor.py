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
        # Direct job detail pages (www or comm subdomain)
        re.compile(r"linkedin\.com/jobs/view/\d+", re.IGNORECASE),
        re.compile(r"linkedin\.com/comm/jobs/view/\d+", re.IGNORECASE),
        # Click-tracking / redirect URLs used in LinkedIn emails
        # e.g. https://click.linkedin-email.com/?qs=...
        re.compile(r"click\.linkedin", re.IGNORECASE),
        # Collections / curated job lists linked in alert emails
        re.compile(r"linkedin\.com/comm/jobs/collections?/", re.IGNORECASE),
        # LinkedIn URL shortener used in some alert emails
        re.compile(r"lnkd\.in/", re.IGNORECASE),
        # Fallback: any linkedin.com/jobs/ sub-path (search pages excluded via EXCLUDE_PATTERNS)
        re.compile(r"linkedin\.com/jobs/[^?]", re.IGNORECASE),
    ],
    "indeed": [
        re.compile(r"indeed\.com/viewjob", re.IGNORECASE),
        re.compile(r"indeed\.com/rc/clk", re.IGNORECASE),
        # Indeed email redirect / tracking links (direct indeed.com paths)
        re.compile(r"indeed\.com/l/", re.IGNORECASE),
        re.compile(r"indeedmail\.com", re.IGNORECASE),
        # Email-specific redirect/tracking domains used in current Indeed job alert emails.
        # Emails from donotreply@jobalert.indeed.com link through these hosts.
        re.compile(r"jobalert\.indeed\.com", re.IGNORECASE),
        re.compile(r"r\.indeed\.com", re.IGNORECASE),
        re.compile(r"click\.indeed\.com", re.IGNORECASE),
    ],
    "trueup": [
        # Direct job pages: trueup.io/jobs/slug or trueup.io/job/slug
        re.compile(r"trueup\.io/job", re.IGNORECASE),
        # Broad catch-all: any trueup.io URL (covers tracking subdomains like
        # click.trueup.io, links.trueup.io used in TrueUp email campaigns).
        # EXCLUDE_PATTERNS still filter unsubscribe/preferences/privacy links.
        re.compile(r"trueup\.io", re.IGNORECASE),
    ],
}

# URL patterns to EXCLUDE (unsubscribe, settings, social links, search-result pages)
EXCLUDE_PATTERNS = [
    re.compile(r"unsubscribe", re.IGNORECASE),
    re.compile(r"email-preferences", re.IGNORECASE),
    re.compile(r"notifications/settings", re.IGNORECASE),
    re.compile(r"manage-settings", re.IGNORECASE),
    re.compile(r"help\.linkedin\.com", re.IGNORECASE),
    re.compile(r"linkedin\.com/legal", re.IGNORECASE),
    re.compile(r"linkedin\.com/jobs\?", re.IGNORECASE),   # search results pages (/jobs?...)
    re.compile(r"linkedin\.com/jobs/$", re.IGNORECASE),   # LinkedIn jobs homepage
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

    # LinkedIn normalization: /comm/jobs/view/ID and /jobs/view/ID are the same job.
    # Strip /comm prefix so both forms produce the same canonical URL.
    path = re.sub(r"^/comm/", "/", parsed.path) if "linkedin.com" in netloc else parsed.path

    # Strip tracking params from query string
    query_params = parse_qs(parsed.query, keep_blank_values=False)
    cleaned_params = {
        k: v for k, v in query_params.items()
        if k.lower() not in TRACKING_PARAMS
    }
    # Sort params for consistent ordering
    clean_query = urlencode(cleaned_params, doseq=True) if cleaned_params else ""

    # Remove fragment
    canonical = urlunparse((scheme, netloc, path, parsed.params, clean_query, ""))

    # Remove trailing slash for consistency
    canonical = canonical.rstrip("/")

    return canonical
