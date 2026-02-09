# File: backend/app/services/jdi/gmail_scanner.py
# Scans Gmail for job alert emails from known sources
import logging
import base64
from datetime import datetime, timezone
from typing import Optional
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

logger = logging.getLogger(__name__)

# Known job alert sender patterns per source
SOURCE_EMAIL_PATTERNS = {
    "linkedin": [
        "jobs-noreply@linkedin.com",
        "jobalerts-noreply@linkedin.com",
    ],
    "indeed": [
        "alert@indeed.com",
        "noreply@indeedmail.com",
    ],
    "trueup": [
        "hello@trueup.io",
        "team@trueup.io",
        "noreply@trueup.io",
    ],
     "other": [
        "jobalert@lb2.recruit.net",
        "no-reply@alerts.talent.com",
        "noreply@glassdoor.com",
        "mailer@jobleads.com",
        "info@trabajo.org",
        "no-reply-jobalert@hrsdc-rhdcc.gc.ca"
    ],
}


def build_search_query(
    sources: Optional[list[str]] = None,
    window_hours: int = 24,
    custom_patterns: Optional[list[str]] = None,
) -> str:
    """
    Build a Gmail search query to find job alert emails.

    Args:
        sources: List of source keys (e.g. ["linkedin", "indeed"]). None = all sources.
        window_hours: How far back to search (default 24h).
        custom_patterns: Additional email patterns to include (user-defined).

    Returns:
        Gmail search query string, e.g.:
        from:(jobs-noreply@linkedin.com OR alert@indeed.com) newer_than:1d
    """
    if sources is None:
        sources = list(SOURCE_EMAIL_PATTERNS.keys())

    # Collect all email addresses for selected sources
    from_addresses = []
    for source in sources:
        addrs = SOURCE_EMAIL_PATTERNS.get(source, [])
        from_addresses.extend(addrs)

    # Add custom patterns if provided (typically when "other" is selected)
    if custom_patterns:
        from_addresses.extend(custom_patterns)

    if not from_addresses:
        logger.warning(f"No email patterns for sources: {sources}")
        return ""

    # Build the from: clause
    from_clause = " OR ".join(from_addresses)

    # Convert window_hours to Gmail's newer_than format
    if window_hours <= 24:
        time_filter = "newer_than:1d"
    elif window_hours <= 168:
        days = max(1, window_hours // 24)
        time_filter = f"newer_than:{days}d"
    else:
        time_filter = "newer_than:7d"

    query = f"from:({from_clause}) {time_filter}"
    logger.debug(f"Gmail search query: {query}")
    return query


def _get_message_body_html(payload: dict) -> str:
    """
    Extract HTML body from Gmail message payload.
    Handles both simple and multipart messages.
    """
    # Check if the message itself has an HTML body
    if payload.get("mimeType") == "text/html":
        data = payload.get("body", {}).get("data", "")
        if data:
            return base64.urlsafe_b64decode(data).decode("utf-8", errors="replace")

    # Multipart: search through parts
    parts = payload.get("parts", [])
    for part in parts:
        mime_type = part.get("mimeType", "")
        if mime_type == "text/html":
            data = part.get("body", {}).get("data", "")
            if data:
                return base64.urlsafe_b64decode(data).decode("utf-8", errors="replace")
        # Nested multipart
        if mime_type.startswith("multipart/"):
            result = _get_message_body_html(part)
            if result:
                return result

    # Fallback to plain text
    for part in parts:
        if part.get("mimeType") == "text/plain":
            data = part.get("body", {}).get("data", "")
            if data:
                return base64.urlsafe_b64decode(data).decode("utf-8", errors="replace")

    return ""


def _get_header(headers: list[dict], name: str) -> str:
    """Extract a specific header value from Gmail message headers."""
    for h in headers:
        if h.get("name", "").lower() == name.lower():
            return h.get("value", "")
    return ""


def fetch_job_alert_emails(
    credentials: Credentials,
    sources: Optional[list[str]] = None,
    window_hours: int = 168,
    max_results: int = 50,
    custom_patterns: Optional[list[str]] = None,
) -> list[dict]:
    """
    Fetch job alert emails from Gmail.

    Args:
        credentials: Authenticated Google OAuth credentials.
        sources: Source filters (e.g. ["linkedin"]). None = all.
        window_hours: How far back to search.
        max_results: Max emails to fetch.
        custom_patterns: Additional email patterns from user profile.

    Returns:
        List of dicts with keys:
        - message_id: Gmail message ID
        - subject: Email subject line
        - from_addr: Sender email address
        - body_html: Email body as HTML string
        - received_at: Datetime when email was received
    """
    query = build_search_query(sources, window_hours, custom_patterns)
    if not query:
        return []

    service = build("gmail", "v1", credentials=credentials)

    # List matching messages
    try:
        results = service.users().messages().list(
            userId="me",
            q=query,
            maxResults=max_results,
        ).execute()
    except Exception as e:
        logger.error(f"Gmail API list error: {e}")
        return []

    messages = results.get("messages", [])
    if not messages:
        logger.info("No job alert emails found")
        return []

    logger.info(f"Found {len(messages)} matching emails")
    logger.debug("sources(normalized)=%s", sources)
    #logger.debug("from_addresses=%s", from_addresses)  # remove unless actually defined here
    logger.info(f"JDI gmail query = {query}")

    # Fetch each message's full content
    email_list = []
    for msg_ref in messages:
        msg_id = msg_ref["id"]
        try:
            msg = service.users().messages().get(
                userId="me",
                id=msg_id,
                format="full",
            ).execute()
        except Exception as e:
            logger.warning(f"Failed to fetch message {msg_id}: {e}")
            continue

        payload = msg.get("payload", {})
        headers = payload.get("headers", [])

        subject = _get_header(headers, "Subject")
        from_addr = _get_header(headers, "From")
        date_str = _get_header(headers, "Date")
        body_html = _get_message_body_html(payload)

        # Parse received_at — Gmail internal date is in ms since epoch
        internal_date = msg.get("internalDate")
        if internal_date:
            received_at = datetime.fromtimestamp(int(internal_date) / 1000, tz=timezone.utc)
        else:
            received_at = datetime.now(timezone.utc)

        email_list.append({
            "message_id": msg_id,
            "subject": subject,
            "from_addr": from_addr,
            "body_html": body_html,
            "received_at": received_at,
        })

    return email_list
