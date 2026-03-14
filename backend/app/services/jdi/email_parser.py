# File: backend/app/services/jdi/email_parser.py
# Parse job listings directly from email HTML, without fetching job posting URLs.
# LinkedIn, Indeed, and TrueUp all block scrapers; but their JOB ALERT EMAILS
# already contain title, company, location, salary, snippet, and the apply link.
import re
import logging
from dataclasses import dataclass, field
from typing import Optional, List

from bs4 import BeautifulSoup, Tag

from app.services.jdi.link_extractor import JOB_URL_PATTERNS, EXCLUDE_PATTERNS

logger = logging.getLogger(__name__)

# Salary pattern for quick line-level detection
_SALARY_RE = re.compile(
    r"(\$[\d,]+|\d+[kK]\b|CA\$[\d,]+|per (hour|hr|yr|year|annum)|salary|compensation|pay range)",
    re.IGNORECASE,
)

# Location keywords
_LOCATION_RE = re.compile(
    r"\b(remote|hybrid|on.?site|canada|usa|united states|"
    r"bc|ontario|alberta|quebec|toronto|vancouver|montreal|calgary|ottawa|"
    r"new york|california|seattle|san francisco|chicago|boston|austin|"
    r"washington|london|uk|berlin|sydney|australia|richmond|burnaby|surrey)\b",
    re.IGNORECASE,
)

# Container tags to look for when crawling up from a link.
# Include <tr> and <table> so we can find sibling rows in LinkedIn-style
# nested-table email layouts (company/location live in a sibling <tr>).
_CONTAINER_TAGS = {"td", "div", "li", "article", "section", "tr", "table"}

# Max container text length — large enough to capture one job card, small
# enough not to grab the whole email body
_MAX_CONTAINER_LEN = 1200

# Separators used by job alert emails to combine company + location on one line
# e.g. "Google · Mountain View, CA"  or  "Amazon - Toronto, ON"
_COMPOUND_SEPS = [" · ", " • ", " | ", " — "]

# Email UI badge/status lines that appear ABOVE the real job title in aggregator
# emails (e.g. Talent.com, Glassdoor). When one of these is anchor_lines[0],
# skip it so the parser uses the next line as the actual job title instead.
# Different from _NAVIGATION_ANCHOR_RE — these lines are not CTAs, just labels.
_BADGE_TITLE_RE = re.compile(
    r"^(talent\.com'?s?\s+pick|closing\s+soon|new\s*!?|featured|promoted|sponsored|"
    r"urgent|hot\s+job|top\s+pick|top\s+job|new\s+match|best\s+match|recommended|"
    r"quickapply|quick\s+apply|actively\s+hiring|just\s+posted|recently\s+posted)$",
    re.IGNORECASE,
)

# Common company-name suffixes — used to detect when a company name is
# accidentally extracted as the job title (Talent.com email format puts company first).
_COMPANY_SUFFIX_RE = re.compile(
    r"\b(group|inc\.?|corp\.?|ltd\.?|llc\.?|plc\.?|solutions|technologies|systems|"
    r"services|consulting|associates|partners|ventures|enterprises|industries|"
    r"holdings|communications|international|global|digital|labs?|studio)\.?\s*$",
    re.IGNORECASE,
)

# Job-title keyword anchors — confirm a line is a job title (not a company name).
_JOB_TITLE_KEYWORD_RE = re.compile(
    r"\b(manager|director|engineer|developer|analyst|coordinator|lead|senior|junior|"
    r"vp|vice\s+president|chief|head\s+of|architect|specialist|consultant|officer|"
    r"associate|intern|supervisor|executive|president|founder|cto|ceo|coo|cfo|"
    r"sre|devops|qa|scrum|product\s+owner|data\s+scientist|ml\s+engineer)\b",
    re.IGNORECASE,
)

# Navigation / UI anchor texts that must NOT be treated as job titles.
# These appear as call-to-action buttons in job alert emails.
_NAVIGATION_ANCHOR_RE = re.compile(
    r"^(view\s+more\s+jobs?|see\s+all\s+jobs?|browse\s+jobs?|find\s+jobs?|"
    r"search\s+jobs?|all\s+jobs?|more\s+jobs?|show\s+more|"
    r"manage\s+settings?|email\s+preferences?|update\s+preferences?|"
    r"notification\s+settings?|alert\s+settings?|"
    r"unsubscribe|opt\s*out|"
    r"sign\s+in|log\s+in|create\s+account|"
    r"create\s+alert|set\s+up\s+alert|new\s+alert|"
    r"get\s+started|learn\s+more|read\s+more|click\s+here|"
    r"view\s+original|view\s+job|apply\s+now|apply\s+here|easily\s+apply|"
    r"view\s+all\s+\d+.*jobs?|view\s+all\s+jobs?|"
    r"see\s+jobs?|view\s+jobs?|"
    r"open\s+in\s+app|download\s+app|get\s+the\s+app|"
    r"follow\s+us|connect\s+with\s+us|"
    r"saved\s+jobs?|my\s+jobs?|job\s+alerts?|"
    # TrueUp digest footer CTAs (not job postings)
    r"hire\s+with\s+\w+|sponsor\s+\w+|my\s+trueup)$",
    re.IGNORECASE,
)


@dataclass
class EmailJobCard:
    """Structured job info parsed from a single job listing in an email."""
    apply_link: str
    title: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    salary_text: Optional[str] = None
    snippet: Optional[str] = None  # Brief description from email body
    source: str = "other"
    email_subject: str = ""  # Job alert search query from email subject line

    def to_scoring_text(self) -> str:
        """Build a text blob for resume scoring."""
        parts = []
        if self.email_subject:
            parts.append(f"Job Alert: {self.email_subject}")
        if self.title:
            parts.append(f"Job Title: {self.title}")
        if self.company:
            parts.append(f"Company: {self.company}")
        if self.location:
            parts.append(f"Location: {self.location}")
        if self.salary_text:
            parts.append(f"Salary: {self.salary_text}")
        if self.snippet:
            parts.append(self.snippet)
        return "\n".join(parts)

    def has_enough_info(self) -> bool:
        """
        Return True only if this looks like a real job card.

        Rejects cards whose title is a navigation/UI element (e.g. "View more
        jobs", "Manage settings") — these slip through when email footer links
        share job-related URL keywords.
        """
        if self.title and _NAVIGATION_ANCHOR_RE.match(self.title.strip()):
            return False
        # Must have at minimum a real title (one word alone is not enough)
        if self.title and len(self.title.split()) < 2:
            return False
        return bool(self.title or self.snippet)


def parse_job_cards(
    html_body: str,
    source: str = "other",
    email_subject: str = "",
) -> List[EmailJobCard]:
    """
    Parse job cards from email HTML body.

    Extracts structured job info (title, company, location, salary, snippet, link)
    directly from the email — no URL fetching required.

    Args:
        html_body: Raw HTML of the job alert email.
        source: Source name (linkedin, indeed, trueup, other).
        email_subject: Email subject line (used as scoring context).

    Returns:
        List of EmailJobCard objects.
    """
    if not html_body:
        return []

    soup = BeautifulSoup(html_body, "html.parser")
    cards = _extract_cards_generic(soup, source, email_subject=email_subject)
    logger.info(f"Parsed {len(cards)} job cards from {source} email")
    return cards


def _extract_cards_generic(
    soup: BeautifulSoup,
    source: str,
    email_subject: str = "",
) -> List[EmailJobCard]:
    """
    Generic card extractor: find all job-matching <a> tags, then harvest
    the surrounding context for title / company / location / salary / snippet.

    Works for LinkedIn, Indeed, TrueUp, and aggregator emails because the
    job link itself is the anchor, and nearby DOM text has the metadata.
    """
    source_patterns = JOB_URL_PATTERNS.get(source, [])
    cards: List[EmailJobCard] = []
    seen_links: set = set()

    for a_tag in soup.find_all("a", href=True):
        href: str = a_tag["href"].strip()
        if not href or href.startswith("mailto:"):
            continue
        if any(p.search(href) for p in EXCLUDE_PATTERNS):
            continue

        # Reject navigation/footer anchors early — before any URL check.
        # This catches "View more jobs", "Manage settings", "See all jobs" etc.
        link_text = a_tag.get_text(strip=True)
        if _NAVIGATION_ANCHOR_RE.match(link_text):
            continue

        # For known sources, only accept matching URL patterns
        if source_patterns:
            if not any(p.search(href) for p in source_patterns):
                continue
        else:
            # For "other" sources: require job-related keywords in the URL only.
            # Accepting based on link text was letting navigation buttons through
            # (e.g. "View more jobs" → text has "jobs" → garbage card created).
            if not re.search(r"(job|career|position|apply|opening|vacancy)", href, re.IGNORECASE):
                continue

        # Deduplicate on link
        if href in seen_links:
            continue
        seen_links.add(href)

        card = _card_from_anchor(a_tag, href, source, email_subject=email_subject)
        if card and card.has_enough_info():
            cards.append(card)

    return cards


def _card_from_anchor(
    a_tag: Tag,
    href: str,
    source: str,
    email_subject: str = "",
) -> Optional[EmailJobCard]:
    """
    Build an EmailJobCard by inspecting an <a> tag and its surrounding context.

    Handles two real-world LinkedIn email layouts:
      (a) Title-only anchor: <a>Job Title</a> <div>Company</div> <div>Location</div>
      (b) Full-card anchor:  <a><span>Job Title</span><span>Company</span>...</a>

    For layout (b), we split the anchor's inner text by newlines so only the
    first line becomes the title and the rest become context lines.
    """
    # Extract all text lines from the anchor, splitting on element boundaries.
    # separator="\n" inserts newlines between inner elements (div, span, strong, etc.)
    # so multi-element anchors yield clean per-field lines.
    raw_anchor = a_tag.get_text(separator="\n", strip=True)
    anchor_lines = [l.strip() for l in raw_anchor.split("\n") if l.strip()]

    # Skip email UI badge/status lines at the front of the anchor text.
    # e.g. "Talent.com's pick\nSenior Director, TPM" → title = "Senior Director, TPM"
    #      "Closing soon\nDirector, Ratings AI"       → title = "Director, Ratings AI"
    while anchor_lines and _BADGE_TITLE_RE.match(anchor_lines[0]):
        anchor_lines = anchor_lines[1:]

    # Detect company-as-title (Talent.com email format sometimes puts the company
    # name first, then the job title on the next line).
    # e.g. ["Devacor Solutions Group", "QA Automation Developer (x5)", "Remote", "$208K"]
    #    → swap so title="QA Automation Developer (x5)", company in context
    if (
        len(anchor_lines) >= 2
        and _COMPANY_SUFFIX_RE.search(anchor_lines[0])
        and _JOB_TITLE_KEYWORD_RE.search(anchor_lines[1])
    ):
        anchor_lines[0], anchor_lines[1] = anchor_lines[1], anchor_lines[0]

    # Title is the first non-empty line inside the anchor (after badge/company fixes)
    title = anchor_lines[0] if anchor_lines else None

    # If title line contains compound separators (e.g. "Title · Company · City"),
    # split to isolate just the job title and push the rest into anchor context.
    if title:
        for sep in _COMPOUND_SEPS:
            if sep in title:
                parts = title.split(sep, 1)
                title = parts[0].strip()
                if len(parts) > 1 and parts[1].strip():
                    # Remaining portion (company · location · salary) becomes context
                    anchor_lines = [title, parts[1].strip()] + anchor_lines[1:]
                break

    # Lines from anchor beyond the title (company, location, salary extracted inline)
    anchor_context = anchor_lines[1:] if len(anchor_lines) > 1 else []

    # Crawl up to find the smallest container that has more text than just the title
    container = _find_container(a_tag, title)

    if container is not None:
        container_lines = [
            line.strip()
            for line in container.get_text(separator="\n").split("\n")
            if line.strip()
        ]
        # Remove lines that exactly match the title (case-insensitive)
        title_lower = (title or "").lower()
        context_lines = [l for l in container_lines if l.lower() != title_lower]
    else:
        # No parent container found — use only lines from inside the anchor
        context_lines = anchor_context

    company, location, salary_text, snippet = _classify_lines(context_lines)

    return EmailJobCard(
        apply_link=href,
        title=title,
        company=company,
        location=location,
        salary_text=salary_text,
        snippet=snippet,
        source=source,
        email_subject=email_subject,
    )


def _find_container(a_tag: Tag, title: Optional[str]) -> Optional[Tag]:
    """
    Walk up the DOM from the <a> tag to find the smallest block element
    that contains more text than just the title alone.

    We intentionally cross <table> boundaries so that LinkedIn-style
    emails (where company/location live in sibling <tr> elements of an
    inner job table) are handled correctly.  We stop only at <body>/<html>.
    A max-length cap (_MAX_CONTAINER_LEN) prevents us from grabbing the
    whole email body.
    """
    title_len = len(title or "")
    for parent in a_tag.parents:
        name = getattr(parent, "name", None)
        if name in ("body", "html"):
            break
        if name in _CONTAINER_TAGS:
            text = parent.get_text(strip=True)
            # Must have meaningfully more text, but not be the whole email
            if title_len + 10 < len(text) < _MAX_CONTAINER_LEN:
                return parent
    return None


def _split_compound_line(line: str) -> tuple[Optional[str], Optional[str]]:
    """
    Split a 'Company · Location' or 'Company - Location' compound line.
    Returns (company, location) or (None, None) if no known separator found.
    Only splits when the right-hand side looks like a real location.
    """
    for sep in _COMPOUND_SEPS:
        if sep in line:
            left, right = line.split(sep, 1)
            left, right = left.strip(), right.strip()
            if left and right and _LOCATION_RE.search(right):
                return left, right
    # Also try a bare " - " split only when the right side looks like a location
    if " - " in line:
        left, right = line.split(" - ", 1)
        left, right = left.strip(), right.strip()
        if left and right and _LOCATION_RE.search(right):
            return left, right
    return None, None


def _classify_lines(lines: List[str]) -> tuple:
    """
    Heuristically classify context lines into company / location / salary / snippet.

    Handles:
    - Plain company lines:          "Google"
    - Compound company+location:    "Google · Mountain View, CA (Remote)"
    - Standalone location lines:    "Vancouver, BC"
    - Salary lines:                 "$150,000 - $200,000/yr"
    - Snippet / description text

    Returns: (company, location, salary_text, snippet)
    """
    company = None
    location = None
    salary_text = None
    snippet_parts: List[str] = []

    for line in lines:
        if len(line) < 2 or line.startswith("http"):
            continue

        # --- Compound "Company · Location" line (check BEFORE salary so a line like
        #     "Stripe · San Francisco, CA · $160K" is split first, then the salary
        #     portion is extracted from the location part if needed) ---
        comp_candidate, loc_candidate = _split_compound_line(line)
        if comp_candidate and loc_candidate:
            if company is None:
                company = comp_candidate
            if location is None:
                # Strip trailing salary from the location segment
                loc_clean = re.split(r"\s[·•|]\s", loc_candidate)[0].strip()
                location = loc_clean
            # If the line also contains salary info, capture it
            if salary_text is None and _SALARY_RE.search(line):
                salary_text = line
            continue

        # --- Salary-only line ---
        if _SALARY_RE.search(line) and salary_text is None:
            salary_text = line
            continue

        # --- Standalone location line ---
        if _LOCATION_RE.search(line) and location is None and len(line) < 100:
            location = line
            continue

        # --- First plain line → company ---
        if company is None and 2 < len(line) < 120:
            company = line
            continue

        # --- Everything else → snippet ---
        if len(line) > 20:
            snippet_parts.append(line)

    snippet = " ".join(snippet_parts[:4]) if snippet_parts else None
    return company, location, salary_text, snippet
