# File: /backend/app/utils/job_extraction.py
# Utility functions for job extraction (JD-only) with PATTERN-DRIVEN extraction

from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass
from typing import Dict, Optional, Tuple, List

from app.config.skills_config import SKILL_KEYWORDS, MIN_SKILL_FREQUENCY, MAX_EMPHASIZED_SKILLS

# --- Optional spaCy (keep it non-fatal) ---
try:
    import spacy  # type: ignore
    try:
        nlp = spacy.load("en_core_web_sm")
    except Exception:
        nlp = None
except Exception:
    nlp = None


# ----------------------------
# Learned Patterns from Gold Data
# ----------------------------

# Words that commonly appear BEFORE the title
TITLE_BEFORE_PATTERNS = [
    "seeking", "seeking a", "seeking an",
    "looking for", "looking for a", "looking for an",
    "hiring", "hiring a", "hiring an",
    "as a", "as an", "as the",
    "join as", "join us as",
    "for a", "for an", "for the",
    "experienced", "visionary",
]

# Words/patterns that commonly appear AFTER the title
TITLE_AFTER_PATTERNS = [
    "to lead", "to join", "to build", "to drive", "to shape",
    ", you will", "you will",
    "reporting to", "who will",
]

# CRITICAL: A valid title MUST contain at least ONE of these role words
# These are the core words that make something a job title
TITLE_MUST_HAVE_WORDS = [
    # Leadership roles
    "director", "manager", "head", "lead", "chief",
    "president", "vp", "vice president", "avp", "svp", "evp",
    "officer", "cto", "cio", "ceo", "cfo", "coo",
    
    # Technical roles (SINGULAR only to avoid "Engineering" matching)
    "engineer", "architect", "developer", "programmer",
    "analyst", "scientist", "specialist", "consultant",
    "administrator", "coordinator", "supervisor",
    
    # Other roles
    "principal", "staff", "senior", "junior", "associate",
]

# Additional role keywords for context (but not required)
ROLE_CONTEXT_KEYWORDS = [
    "engineering", "software", "quality", "qa", "qe", "sdet",
    "platform", "devops", "infrastructure", "security",
    "data", "ml", "ai", "product", "technical", "technology"
]

# Junk headings to exclude
HEADING_JUNK = {
    "about the job", "job description", "company description", "team description", 
    "role description", "overview", "responsibilities", "qualifications", 
    "requirements", "required", "preferred",
    "what you'll do", "what you will do",
    "what you'll bring", "what you will bring",
    "the opportunity", "the team", "you will", "you are",
    "success indicators", "key responsibilities", "summary",
    "the role", "the position", "who we are", "about us"
}

COMPANY_BAD_WORDS = {
    "job", "jobs", "role", "position", "team", "engineering", "software", 
    "technology", "requirements", "qualifications", "responsibilities", 
    "overview", "ai", "react", "oracle", ".net", "c#", "background",
    "building", "going", "key responsibilities", "the opportunity", 
    "us", "the company", "our company", "our mission", "our team",
    "the role", "the position", "who we are", "about the",
    "culture", "description", "summary"
}


# ----------------------------
# Helper Functions
# ----------------------------

def _clean_spaces(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").strip())


def _norm(s: str) -> str:
    return _clean_spaces(s).lower()


def _sanitize_single_line(value: str, max_len: int) -> str:
    """Force single-line output, trim, and cap length."""
    v = (value or "").replace("\r", "\n")
    parts = [_clean_spaces(x) for x in v.split("\n") if _clean_spaces(x)]
    v = _clean_spaces(" ".join(parts))
    if len(v) > max_len:
        v = v[:max_len].rstrip()
    return v


def _get_context_window(text: str, match_start: int, match_end: int, words_before: int = 5, words_after: int = 5) -> Tuple[str, str]:
    """
    Extract N words before and after a match position.
    Returns (before_text, after_text)
    """
    before = text[:match_start]
    after = text[match_end:]
    
    before_words = before.split()[-words_before:] if before else []
    after_words = after.split()[:words_after] if after else []
    
    return " ".join(before_words), " ".join(after_words)


def _clean_title_output(title: str) -> str:
    """
    Polish the extracted title:
    - Remove "as a", "as an", "as the"
    - Remove "at [Company]" suffix
    - Remove trailing punctuation
    - Strip location/remote tags
    - STOP at natural boundaries where description begins
    """
    if not title:
        return ""
    
    # Remove leading articles and adjectives
    title = re.sub(r"(?i)^(as a|as an|as|as the|and|an|a|the|experienced|hands-on|visionary|dynamic|talented|seasoned|successful|highly motivated|detail-oriented|strategic)\s+", "", title.strip())
    
    # STOP at boundaries - split and take first part only
    # Pattern: ", you" or "you'll" or "you will"
    if re.search(r",?\s+you['â€™\s]*(will|ll|are)", title, re.IGNORECASE):
        title = re.split(r",?\s+you['â€™\s]*(will|ll|are)", title, flags=re.IGNORECASE)[0]
    
    # Pattern: "to [verb]"
    if re.search(r"\s+to\s+(lead|join|build|drive|shape|define|help|partner)", title, re.IGNORECASE):
        title = re.split(r"\s+to\s+(lead|join|build|drive|shape|define|help|partner)", title, flags=re.IGNORECASE)[0]
    
    # Pattern: "for our/the"
    if re.search(r"\s+for\s+(our|the)\s", title, re.IGNORECASE):
        title = re.split(r"\s+for\s+(our|the)\s", title, flags=re.IGNORECASE)[0]
    
    # Pattern: "with consulting/experience"
    if re.search(r"\s+with\s+(consulting|experience)", title, re.IGNORECASE):
        title = re.split(r"\s+with\s+(consulting|experience)", title, flags=re.IGNORECASE)[0]

    # Pattern: "focused on"
    if re.search(r"\s+focused\s+on", title, re.IGNORECASE):
        title = re.split(r"\s+focused\s+on", title, flags=re.IGNORECASE)[0]

    # Pattern: "is a senior ..."
    if re.search(r"\s+is\s+a\s+(senior)?", title, re.IGNORECASE):
        title = re.split(r"\s+is\s+a", title, flags=re.IGNORECASE)[0]

    
    # Remove "at [Company]" suffix
    title = re.split(r"\s+[Aa]t\s+", title)[0]
    
    # Remove location/remote tags
    title = re.sub(r"\s*\((remote|hybrid|on[-\s]?site|onsite).*?\)\s*$", "", title, flags=re.IGNORECASE)
    
    # Remove pipes and dashes
    title = re.split(r"[\(\|]", title)[0]
    title = re.split(r"\s+[—–-]\s+", title)[0]
    
    # Clean trailing punctuation
    title = title.strip().strip(',').strip(':').strip('.')

    # Remove trailing verbs/descriptions
    title = re.split(r'\s+(for|to|will|you will|you\'ll|for our|to| is a senior|offers|specializes)', title)[0].strip()
    
    return _clean_spaces(title)


def _has_title_role_word(text: str) -> bool:
    """
    Check if text contains at least ONE required role word.
    This ensures we're extracting actual titles, not random phrases.
    """
    text_lower = text.lower()
    
    # Check for MUST_HAVE words (these make it a title)
    for word in TITLE_MUST_HAVE_WORDS:
        # Use word boundary to avoid partial matches
        if re.search(r'\b' + re.escape(word) + r'\b', text_lower):
            return True
    
    return False


def _is_complete_title(text: str) -> bool:
    """
    Validate that this looks like a COMPLETE title, not a fragment.
    
    A complete title should:
    1. Have at least ONE MUST_HAVE role word (Director, Manager, Engineer, etc.)
    2. Not be a description or qualification
    3. Actually look like a job title structure
    """
    if not text or len(text) < 5:
        return False
    
    text_lower = text.lower().strip()
    words = text_lower.split()
    
    # CRITICAL: Must have at least ONE required role word
    if not _has_title_role_word(text):
        return False
    
    # Should not be a description phrase
    description_indicators = [
        "leader of", "leader in",
        "leading", "experience", "reporting to", "directly to",
        "serve as", "serves as", "responsible for",
        "headquartered", "based in", "located in",
        "will be", "will work", "will lead",
        "you will", "who will", "we are", "who we are",
        # Add specific failures from screenshots
        "to define", "training sessions", "by example",
        "successful candidate", "similar role"
    ]
    
    for indicator in description_indicators:
        if indicator in text_lower:
            return False
    
    # Check word count (titles are typically 2-10 words)
    if len(words) < 2 or len(words) > 12:
        return False
    
    # Check if it starts with a verb (likely a responsibility, not title)
    # BUT allow "Lead" and "Architect" as they can be titles
    verb_starts = ["define", "execute", "build", "develop", "ensure", "orchestrate", 
                   "drive", "manage", "oversee", "provide", "create", "deliver",
                   "establish", "implement", "coordinate", "support", "enhance"]
    
    if words[0] in verb_starts and len(words) > 5:
        return False
    
    # Reject if it's just the role word alone
    if len(words) == 1 and words[0] in TITLE_MUST_HAVE_WORDS:
        return False
    
    return True


def _is_heading_junk(text: str) -> bool:
    """Check if text is a common heading."""
    text_lower = _norm(text)
    return text_lower in HEADING_JUNK


def _looks_like_sentence(text: str) -> bool:
    """Check if text looks like a sentence (has verbs, ends with period)."""
    if '.' in text and not text.strip().endswith('.'):
        # Period in middle = likely sentence
        return True
    
    # Check for verb patterns at start
    verb_starts = ["define", "execute", "build", "develop", "ensure", "orchestrate", 
                   "drive", "lead", "manage", "oversee", "provide", "create"]
    
    words = text.lower().split()
    if words and words[0] in verb_starts and len(words) > 6:
        return True
    
    return False


# ----------------------------
# Title Extraction - Pattern-Driven Engine
# ----------------------------

@dataclass
class TitleCandidate:
    text: str
    score: float
    line_num: int
    position: int
    before_context: str
    after_context: str


def extract_title(text: str) -> str:
    """
    Pattern-driven title extraction based on gold data analysis.
    
    Strategy:
    1. Search first 20 lines for title-shaped phrases
    2. Score based on learned patterns (words before/after)
    3. Validate with MUST_HAVE role keywords
    4. Return highest-scoring candidate that passes validation
    """
    if not text:
        return "Unknown Title"
    
    # Get first 20 lines (titles are usually in first 10, but scan 20 to be safe)
    lines = [l.strip() for l in text.split('\n') if l.strip()][:20]
    
    if not lines:
        return "Unknown Title"
    
    # Priority 1: Check for explicit headers (e.g., "Job Title: Director")
    for line in lines[:5]:
        match = re.search(r"(?i)^(job title|position|role)\s*[:|-]\s*(.+)$", line)
        if match:
            title = _clean_title_output(match.group(2).split('\n')[0])
            if _is_complete_title(title) and 5 < len(title) < 100:
                return title
    
    # Priority 2: Pattern-based extraction with sliding windows
    candidates: List[TitleCandidate] = []
    
    # Build full text for pattern matching (first 2000 chars)
    full_text = "\n".join(lines)[:2000]
    
    # Search for titles using sliding window (2-10 words)
    words = full_text.split()
    
    # Try longer windows first to capture complete titles
    for window_size in range(10, 1, -1):  # 10, 9, 8, ... 2
        for i in range(len(words) - window_size + 1):
            phrase = ' '.join(words[i:i + window_size])
            
            # Quick filters
            if len(phrase) < 6 or len(phrase) > 150:
                continue
            
            # CRITICAL: Must be a complete title with required role word
            if not _is_complete_title(phrase):
                continue
            
            if _is_heading_junk(phrase):
                continue
            
            if _looks_like_sentence(phrase):
                continue
            
            # Get position in text
            match_start = full_text.find(phrase)
            if match_start == -1:
                continue
            
            match_end = match_start + len(phrase)
            
            # Get context
            before_ctx, after_ctx = _get_context_window(full_text, match_start, match_end, words_before=8, words_after=8)
            
            # Calculate score
            score = _score_title_candidate(
                candidate=phrase,
                position=match_start,
                before_context=before_ctx,
                after_context=after_ctx,
                text_length=len(full_text)
            )
            
            # Find which line this is on
            line_num = full_text[:match_start].count('\n') + 1
            
            candidates.append(TitleCandidate(
                text=phrase,
                score=score,
                line_num=line_num,
                position=match_start,
                before_context=before_ctx,
                after_context=after_ctx
            ))
    
    # Return best candidate
    if candidates:
        candidates.sort(key=lambda x: x.score, reverse=True)
        
        # Take best candidate that passes validation
        for candidate in candidates[:5]:  # Check top 5
            cleaned = _clean_title_output(candidate.text)
            if _is_complete_title(cleaned) and candidate.score > 20:
                return cleaned
    
    return "Unknown Title"


def _score_title_candidate(candidate: str, position: int, before_context: str, 
                           after_context: str, text_length: int) -> float:
    """
    Score a title candidate based on learned patterns.
    Higher score = more likely to be the actual title.
    """
    score = 0.0
    candidate_lower = candidate.lower()
    before_lower = before_context.lower()
    after_lower = after_context.lower()
    
    # 1. POSITION SCORING (earlier is better)
    # Titles usually appear in first 500 chars
    if position < 100:
        score += 50
    elif position < 300:
        score += 30
    elif position < 500:
        score += 15
    else:
        score += max(0, 10 - (position - 500) / 100)
    
    # 2. BEFORE CONTEXT PATTERNS (learned from gold data)
    for pattern in TITLE_BEFORE_PATTERNS:
        if pattern in before_lower:
            score += 40  # Strong signal!
            break
    
    # 3. AFTER CONTEXT PATTERNS (learned from gold data)
    for pattern in TITLE_AFTER_PATTERNS:
        if pattern in after_lower:
            score += 25  # Good signal
            break
    
    # 4. TITLE STRUCTURE
    # Titles with "Director, Engineering" or "Director of Engineering"
    if ',' in candidate or ' of ' in candidate_lower or ' / ' in candidate:
        score += 20
    
    # Seniority keywords
    if any(word in candidate_lower for word in ['senior', 'sr', 'vp', 'vice president', 'head', 'avp', 'principal', 'chief', 'lead']):
        score += 15
    
    # 5. LENGTH (optimal title length is 15-60 chars)
    length = len(candidate)
    if 15 <= length <= 60:
        score += 10
    elif 10 <= length <= 80:
        score += 5
    else:
        score -= 10
    
    # 6. WORD COUNT (2-6 words is typical)
    word_count = len(candidate.split())
    if 2 <= word_count <= 6:
        score += 15
    elif word_count == 7 or word_count == 8:
        score += 5  # Still okay
    elif word_count > 8:
        score -= 20  # Too long = likely a sentence
    
    # 7. CAPITALIZATION (titles are usually Title Case)
    if candidate[0].isupper():
        score += 5
    
    # 8. HAS MUST_HAVE WORD BONUS
    if _has_title_role_word(candidate):
        score += 25
    
    # 9. NEGATIVE PATTERNS
    # Penalize if it looks like a sentence
    if candidate.endswith('.') or candidate.endswith(':'):
        score -= 30
    
    # Penalize if starts with verb
    first_word = candidate.split()[0].lower()
    if first_word in ['define', 'execute', 'build', 'develop', 'ensure', 'drive', 'manage', 'oversee']:
        if word_count > 5:  # "Build Engineer" is OK, "Build and manage teams" is not
            score -= 40
    
    # Penalize description words
    description_words = ['leader', 'strategic', 'technical', 'mentor', 'experience', 'reporting']
    if any(word in candidate_lower for word in description_words):
        score -= 35
    
    return score


# ----------------------------
# Company Extraction - IMPROVED
# ----------------------------

def _is_valid_company_name(text: str) -> bool:
    """
    Validate that extracted text looks like an actual company name.
    
    Rules:
    - Should be 2-50 characters
    - Should start with capital letter or number
    - Should not be common junk phrases
    - Should not contain verbs/action words
    - Should not be generic phrases
    """
    if not text or len(text) < 2 or len(text) > 50:
        return False
    
    text_lower = text.lower().strip()
    
    # Must start with capital or number
    if not (text[0].isupper() or text[0].isdigit()):
        return False
    
    # Check against junk phrases
    junk_phrases = {
        "the team", "the role", "the position", "the opportunity",
        "the job", "the company", "our team", "our mission",
        "our company", "about us", "who we are", "what we do",
        "summary", "description", "overview"
    }
    
    if text_lower in junk_phrases:
        return False
    
    # Should not contain these words
    bad_indicators = [
        "acquires", "powers", "support", "makes", "break", "empowers",
        "transcend", "enhance", "our developers", "people around",
        "strategy", "home", "way", "culture"
    ]
    
    for indicator in bad_indicators:
        if indicator in text_lower:
            return False
    
    # Should not have verbs in present tense
    verb_patterns = [
        r'\b(is|are|was|were|will|can|may|should|has|have|had)\b',
        r'\b(provides|builds|helps|makes|offers|creates|develops)\b',
        r'\b(going|doing|working|building|creating)\b'
    ]
    
    for pattern in verb_patterns:
        if re.search(pattern, text_lower):
            return False
    
    # Word count check (company names are usually 1-5 words)
    words = text.split()
    if len(words) > 6:
        return False
    
    return True


def extract_company_name(text: str, known_companies: List[str] = None) -> str:
    """
    Improved JD-only company extraction with better validation.
    """
    if not text:
        return "Unknown Company"

    # Priority 0: Known companies lookup (most reliable)
    if known_companies:
        for co in sorted(known_companies, key=len, reverse=True):
            if isinstance(co, str) and len(co) > 2:
                # Look for exact company name in first 2000 chars
                if re.search(r'\b' + re.escape(co) + r'\b', text[:2000], re.IGNORECASE):
                    return _clean_spaces(co)

    # Priority 1: "About [Company]" pattern (very high confidence)
    about_match = re.search(r"(?i)About\s+([A-Z][A-Za-z0-9\s&\.]+?)(?:\s*\n|:|$)", text[:1500])
    if about_match:
        cand = about_match.group(1).strip()
        # Remove trailing noise
        cand = re.split(r'\s+(is|was|are|were|has|have|provides|offers|specializes)', cand)[0].strip()
        if _is_valid_company_name(cand):
            return _clean_spaces(cand)

    # Priority 2: Company name at start of JD (e.g., "Acme Corp is a leading...")
    # Look in first 200 chars for company name followed by "is/provides/offers/etc"
    first_lines = text[:200]
    company_intro = re.search(r'^([A-Z][A-Za-z0-9\s&\.]{2,40}?)\s+(is|provides|offers|specializes|builds|empowers|pioneers|helps|makes|enables)', first_lines, re.MULTILINE)
    if company_intro:
        cand = company_intro.group(1).strip()
        if _is_valid_company_name(cand):
            return _clean_spaces(cand)

    # Priority 3: "At [Company]," pattern
    at_match = re.search(r"(?i)At\s+([A-Z][A-Za-z0-9\s&\.]{2,40}?)[,:\n]", text[:1000])
    if at_match:
        cand = at_match.group(1).strip()
        if _is_valid_company_name(cand) and cand.lower() not in COMPANY_BAD_WORDS:
            return _clean_spaces(cand)

    # Priority 4: Look for company name in capitalized phrases
    # Scan first 1000 chars for Title Case phrases
    lines = text[:1000].split('\n')[:10]
    for line in lines:
        # Look for sequences of Title Case words
        title_case_match = re.search(r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,3})\b', line)
        if title_case_match:
            cand = title_case_match.group(1).strip()
            if _is_valid_company_name(cand):
                # Extra validation - should not be common words
                common_words = {'About', 'The', 'This', 'Our', 'We', 'Job', 'Role', 'Position', 'Team'}
                if not any(word in cand.split() for word in common_words):
                    return _clean_spaces(cand)

    return "Unknown Company"


# ----------------------------
# Other Extraction Functions (Unchanged)
# ----------------------------

def extract_salary(job_description: str) -> Optional[str]:
    if not job_description:
        return None

    patterns = [
        r"\$\s?\d{2,3}(?:,\d{3})?\s*[-—–]\s*\$\s?\d{2,3}(?:,\d{3})?",
        r"\$\s?\d{2,3}K\s*[-—–]\s*\$\s?\d{2,3}K",
        r"\$\s?\d{2,3}(?:,\d{3})?\s*(?:per year|annually|/year)",
        r"\$\s?\d{2,3}K\s*(?:per year|annually|/year)",
        r"\$\s?\d{2,3}(?:,\d{3})?",
        r"\$\s?\d{2,3}K",
    ]

    for pattern in patterns:
        m = re.search(pattern, job_description, re.IGNORECASE)
        if m:
            return m.group(0).strip()

    return None


def extract_years_experience(text: str) -> str:
    if not text:
        return "Unspecified"
    m = re.search(r"\b\d+\+?\s+years?\b", text, re.IGNORECASE)
    return m.group(0).strip() if m else "Unspecified"


def extract_location(text: str) -> str:
    if not text:
        return "Unspecified"

    # High-signal patterns
    m = re.search(r"(?i)\b(canada\s*\(remote\)|remote\s*\(canada\)|canada\s*-\s*remote)\b", text)
    if m:
        return _clean_spaces(m.group(0))

    # City, Province patterns
    m = re.search(r"\b([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)*),\s*(BC|ON|QC|AB|MB|SK|NS|NB|NL|PE)\b", text)
    if m:
        return _clean_spaces(m.group(0))

    # spaCy fallback
    if nlp is not None:
        try:
            doc = nlp(text[:5000])
            for ent in doc.ents:
                if ent.label_ in {"GPE", "LOC"}:
                    return ent.text.strip()
        except Exception:
            pass

    return "Unspecified"


def extract_skills_with_frequency(text: str) -> Dict[str, int]:
    if not text:
        return {}

    t = text.lower()
    freq: Dict[str, int] = {}

    skills = SKILL_KEYWORDS.keys() if isinstance(SKILL_KEYWORDS, dict) else SKILL_KEYWORDS

    for skill in skills:
        if not skill:
            continue
        pattern = r"\b" + re.escape(skill.lower()) + r"\b"
        count = len(re.findall(pattern, t))
        if count > 0:
            freq[str(skill)] = count

    return freq


def get_emphasized_skills(extracted_skills: Dict[str, int]) -> Dict[str, int]:
    if not extracted_skills:
        return {}

    emphasized = {k: v for k, v in extracted_skills.items() if v >= MIN_SKILL_FREQUENCY}
    sorted_items = sorted(emphasized.items(), key=lambda x: x[1], reverse=True)
    return dict(sorted_items[:MAX_EMPHASIZED_SKILLS])


def extract_experience(text: str) -> str:
    match = re.search(r"\d+\+?\s+years?", text)
    return match.group(0).strip() if match else "Unspecified"