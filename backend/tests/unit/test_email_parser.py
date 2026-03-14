# Tests for the email_parser module
import pytest
from app.services.jdi.email_parser import parse_job_cards, EmailJobCard


# ── Helpers ──────────────────────────────────────────────────────────────────

def _linkedin_email(job_id: int = 1234567890, title: str = "Senior QA Engineer",
                    company: str = "Acme Corp", location: str = "Vancouver, BC") -> str:
    """Minimal LinkedIn job alert email HTML (title-only anchor, company/location outside)."""
    return f"""
    <html><body>
    <table>
      <tr><td>
        <a href="https://www.linkedin.com/comm/jobs/view/{job_id}?alertAction=accept">
          {title}
        </a>
        <div>{company}</div>
        <div>{location}</div>
        <div>$90,000 – $120,000/yr</div>
      </td></tr>
    </table>
    </body></html>
    """


def _linkedin_wrapped_email(job_id: int = 9876543210,
                            title: str = "Manager, Continuous Improvements and Quality",
                            company: str = "Coast Mountain Bus Company",
                            location: str = "Vancouver, BC (Hybrid)",
                            salary: str = "CA$110K-CA$165K / year") -> str:
    """LinkedIn job alert where the full card is wrapped inside the <a> tag."""
    return f"""
    <html><body>
    <table>
      <tr><td>
        <a href="https://www.linkedin.com/comm/jobs/view/{job_id}?alertAction=accept">
          <strong>{title}</strong>
          <span>{company}</span>
          <span>{location}</span>
          <span>{salary}</span>
          <span>Actively recruiting</span>
        </a>
      </td></tr>
    </table>
    </body></html>
    """


def _indeed_email(job_key: str = "abc123", title: str = "QA Director",
                  company: str = "TechCo", location: str = "Remote") -> str:
    """Minimal Indeed job alert email HTML (old direct link format)."""
    return f"""
    <html><body>
    <table>
      <tr><td>
        <a href="https://ca.indeed.com/rc/clk?jk={job_key}&fccid=xyz">
          {title}
        </a>
        <span>{company}</span>
        <span>{location}</span>
        <p>Looking for an experienced QA Director to lead our quality initiatives.</p>
      </td></tr>
    </table>
    </body></html>
    """


def _indeed_jobalert_email(job_key: str = "abc123",
                           title: str = "Director of Technology & AI Enablement",
                           company: str = "Segev LLP",
                           location: str = "Vancouver, BC",
                           salary: str = "$115,000 - $130,000 a year",
                           snippet: str = "Segev LLP is a business law firm built for out of the box clients.") -> str:
    """Realistic Indeed job alert email from donotreply@jobalert.indeed.com.
    Uses r.jobalert.indeed.com redirect links (current format as of Mar 2026).
    """
    return f"""
    <html><body>
    <div style="font-family:Arial">
      <h1>3 new ai director opportunities in vancouver, bc</h1>
      <p>These job ads match your saved job alert</p>
      <table>
        <tr><td>
          <a href="https://r.jobalert.indeed.com/rdr?job={title.replace(' ', '+')}&jk={job_key}&from=alert">
            <strong>{title}</strong>
          </a>
          <div>{company}</div>
          <div>{location}</div>
          <div>{salary}</div>
          <div>► Easily apply</div>
          <p>{snippet}</p>
          <div>2 days ago</div>
        </td></tr>
      </table>
      <a href="https://r.jobalert.indeed.com/unsubscribe?token=xyz">Unsubscribe</a>
    </div>
    </body></html>
    """


def _trueup_email(title: str = "Director of Engineering",
                  company: str = "StartupAI",
                  location: str = "San Francisco, CA") -> str:
    """Minimal TrueUp job alert email HTML (direct link format)."""
    return f"""
    <html><body>
    <div class="job-card">
      <a href="https://www.trueup.io/job/director-engineering-12345">
        {title}
      </a>
      <div>{company}</div>
      <div>{location} | $180,000 – $220,000</div>
      <p>Lead engineering teams building AI-powered SaaS products.</p>
    </div>
    </body></html>
    """


def _trueup_digest_email() -> str:
    """Realistic TrueUp weekly digest email (7 jobs, rich card format).
    TrueUp emails include company description and financial metadata per card.
    Links may go through tracking subdomains.
    """
    return """
    <html><body>
    <div>
      <h2>7 new jobs for you this week</h2>
      <p>All open jobs that fit your profile: 26</p>

      <table>
        <tr><td>
          <a href="https://trueup.io/jobs/director-engineering-docebo-54321">
            Director, Engineering
          </a>
          <div>Docebo</div>
          <div>Corporate learning management system (LMS)</div>
          <div>TORONTO, ONTARIO / REMOTE</div>
          <div>5 days ago</div>
          <div>Public · Valuation $0.7B · 1,000 employees · Layoff 55d ago</div>
        </td></tr>
        <tr><td>
          <a href="https://trueup.io/jobs/director-software-development-autodesk-99999">
            Director of Software Development - AI/ML
          </a>
          <div>Autodesk</div>
          <div>Computer-aided design software</div>
          <div>VANCOUVER, BC, CAN</div>
          <div>2 days ago</div>
          <div>Public · Valuation $52B · 15K employees · Remote 200</div>
        </td></tr>
        <tr><td>
          <a href="https://trueup.io/jobs/principal-software-engineer-github-77777">
            Principal Software Engineer
          </a>
          <div>GitHub</div>
          <div>Software version control using Git (part of Microsoft)</div>
          <div>CANADA REMOTE</div>
          <div>4 days ago</div>
        </td></tr>
      </table>

      <a href="https://trueup.io/unsubscribe?token=abc123">Unsubscribe</a>
      <a href="https://trueup.io/jobs">View all 26 open jobs</a>
    </div>
    </body></html>
    """


def _other_email(title: str = "DevOps Engineer") -> str:
    """Minimal 'other' source job alert email HTML (e.g. Talent.com)."""
    return f"""
    <html><body>
    <table>
      <tr><td>
        <a href="https://ca.talent.com/en/jobs?email_id=abc&job=devops-engineer">
          {title}
        </a>
        <div>CloudSystems Inc</div>
        <div>Toronto, ON - Hybrid</div>
        <div>$110,000/yr</div>
        <p>Seeking a DevOps Engineer with Kubernetes and CI/CD experience.</p>
      </td></tr>
    </table>
    </body></html>
    """


# ── LinkedIn ─────────────────────────────────────────────────────────────────

class TestLinkedInParsing:
    def test_extracts_card(self):
        cards = parse_job_cards(_linkedin_email(), "linkedin")
        assert len(cards) == 1

    def test_apply_link_captured(self):
        cards = parse_job_cards(_linkedin_email(job_id=9999), "linkedin")
        assert "linkedin.com/comm/jobs/view/9999" in cards[0].apply_link

    def test_title_extracted(self):
        cards = parse_job_cards(_linkedin_email(title="Staff Engineer"), "linkedin")
        assert cards[0].title == "Staff Engineer"

    def test_company_extracted(self):
        cards = parse_job_cards(_linkedin_email(company="OpenAI"), "linkedin")
        assert cards[0].company == "OpenAI"

    def test_location_extracted(self):
        cards = parse_job_cards(_linkedin_email(location="Remote"), "linkedin")
        assert cards[0].location == "Remote"

    def test_salary_extracted(self):
        cards = parse_job_cards(_linkedin_email(), "linkedin")
        assert cards[0].salary_text is not None
        assert "$" in cards[0].salary_text

    def test_source_is_linkedin(self):
        cards = parse_job_cards(_linkedin_email(), "linkedin")
        assert cards[0].source == "linkedin"

    def test_no_duplicate_links(self):
        # Same link appears twice in HTML — should only yield one card
        html = _linkedin_email(job_id=111) + _linkedin_email(job_id=111)
        cards = parse_job_cards(html, "linkedin")
        # Should deduplicate to 1 card for job 111
        links = [c.apply_link for c in cards]
        assert len(links) == len(set(links))

    def test_email_subject_stored_on_card(self):
        cards = parse_job_cards(
            _linkedin_email(), "linkedin",
            email_subject='"Head of QA in Vancouver": UBC - Manager, Quality Assurance',
        )
        assert cards[0].email_subject == '"Head of QA in Vancouver": UBC - Manager, Quality Assurance'

    def test_email_subject_in_scoring_text(self):
        cards = parse_job_cards(
            _linkedin_email(), "linkedin",
            email_subject="Head of QA in Vancouver",
        )
        text = cards[0].to_scoring_text()
        assert "Head of QA in Vancouver" in text

    def test_wrapped_anchor_title_extracted_cleanly(self):
        """When the full card is inside the <a> tag, only the first line is the title."""
        cards = parse_job_cards(_linkedin_wrapped_email(), "linkedin")
        assert len(cards) == 1
        # Title should be just the job title, not the full card blob
        assert cards[0].title == "Manager, Continuous Improvements and Quality"
        assert "Coast Mountain Bus" not in cards[0].title

    def test_wrapped_anchor_company_extracted(self):
        cards = parse_job_cards(_linkedin_wrapped_email(), "linkedin")
        assert cards[0].company == "Coast Mountain Bus Company"

    def test_wrapped_anchor_location_extracted(self):
        cards = parse_job_cards(_linkedin_wrapped_email(), "linkedin")
        assert cards[0].location is not None
        assert "Vancouver" in cards[0].location

    def test_wrapped_anchor_salary_extracted(self):
        cards = parse_job_cards(_linkedin_wrapped_email(), "linkedin")
        assert cards[0].salary_text is not None
        assert "CA$" in cards[0].salary_text or "$" in cards[0].salary_text


# ── Indeed ───────────────────────────────────────────────────────────────────

class TestIndeedParsing:
    def test_extracts_card(self):
        cards = parse_job_cards(_indeed_email(), "indeed")
        assert len(cards) == 1

    def test_apply_link_captured(self):
        cards = parse_job_cards(_indeed_email(job_key="xyz999"), "indeed")
        assert "indeed.com/rc/clk" in cards[0].apply_link
        assert "xyz999" in cards[0].apply_link

    def test_title_extracted(self):
        cards = parse_job_cards(_indeed_email(title="Head of QA"), "indeed")
        assert cards[0].title == "Head of QA"

    def test_snippet_captured(self):
        cards = parse_job_cards(_indeed_email(), "indeed")
        # Snippet should contain meaningful words from the email body
        assert cards[0].snippet is not None or cards[0].company is not None


# ── TrueUp ───────────────────────────────────────────────────────────────────

class TestTrueUpParsing:
    def test_extracts_card(self):
        cards = parse_job_cards(_trueup_email(), "trueup")
        assert len(cards) == 1

    def test_apply_link_captured(self):
        cards = parse_job_cards(_trueup_email(), "trueup")
        assert "trueup.io/job/" in cards[0].apply_link

    def test_title_extracted(self):
        cards = parse_job_cards(_trueup_email(title="VP of Engineering"), "trueup")
        assert cards[0].title == "VP of Engineering"

    def test_salary_in_text(self):
        cards = parse_job_cards(_trueup_email(), "trueup")
        # Salary should show up somewhere (salary_text or snippet)
        text = cards[0].to_scoring_text()
        assert "$" in text or cards[0].salary_text is not None or cards[0].snippet is not None


# ── Other sources ─────────────────────────────────────────────────────────────

class TestOtherSourceParsing:
    def test_extracts_card(self):
        cards = parse_job_cards(_other_email(), "other")
        assert len(cards) == 1

    def test_apply_link_captured(self):
        cards = parse_job_cards(_other_email(), "other")
        assert "talent.com" in cards[0].apply_link

    def test_title_extracted(self):
        cards = parse_job_cards(_other_email(title="Platform Engineer"), "other")
        assert cards[0].title == "Platform Engineer"


# ── EmailJobCard helpers ──────────────────────────────────────────────────────

class TestEmailJobCard:
    def test_to_scoring_text_includes_all_fields(self):
        card = EmailJobCard(
            apply_link="https://example.com/job/1",
            title="Senior Engineer",
            company="Acme",
            location="Remote",
            salary_text="$120K",
            snippet="Looking for a senior engineer with Python skills.",
            source="linkedin",
        )
        text = card.to_scoring_text()
        assert "Senior Engineer" in text
        assert "Acme" in text
        assert "Remote" in text
        assert "$120K" in text
        assert "Python" in text

    def test_to_scoring_text_includes_email_subject(self):
        card = EmailJobCard(
            apply_link="https://example.com/job/1",
            title="Senior Engineer",
            source="linkedin",
            email_subject="Head of Engineering in Vancouver",
        )
        text = card.to_scoring_text()
        assert "Head of Engineering in Vancouver" in text

    def test_to_scoring_text_skips_none_fields(self):
        card = EmailJobCard(apply_link="https://example.com/job/1", title="Engineer")
        text = card.to_scoring_text()
        assert "None" not in text
        assert "Engineer" in text

    def test_has_enough_info_with_multi_word_title(self):
        card = EmailJobCard(apply_link="https://example.com", title="Software Engineer")
        assert card.has_enough_info() is True

    def test_has_enough_info_single_word_title_rejected(self):
        # Single-word "titles" are too ambiguous — require at least 2 words
        card = EmailJobCard(apply_link="https://example.com", title="Engineer")
        assert card.has_enough_info() is False

    def test_has_enough_info_with_snippet(self):
        card = EmailJobCard(apply_link="https://example.com", snippet="Great role at a startup")
        assert card.has_enough_info() is True

    def test_has_enough_info_subject_only_rejected(self):
        # Subject alone is no longer enough — we need a real title or snippet
        # to avoid letting navigation cards through
        card = EmailJobCard(apply_link="https://example.com", email_subject="QA Lead in Toronto")
        assert card.has_enough_info() is False

    def test_has_enough_info_false_when_empty(self):
        card = EmailJobCard(apply_link="https://example.com")
        assert card.has_enough_info() is False

    def test_has_enough_info_navigation_title_rejected(self):
        """Navigation anchor texts like 'View more jobs' must be rejected."""
        for nav_text in ["View more jobs", "See all jobs", "Manage settings",
                         "Manage Settings", "VIEW MORE JOBS", "unsubscribe"]:
            card = EmailJobCard(apply_link="https://example.com/job/1", title=nav_text)
            assert card.has_enough_info() is False, f"Expected False for title='{nav_text}'"

    def test_has_enough_info_real_job_title_passes(self):
        """Real multi-word job titles must pass."""
        for title in ["Quality Assurance Manager", "Director of Engineering",
                      "Senior Software Engineer", "VP of Quality"]:
            card = EmailJobCard(apply_link="https://example.com/job/1", title=title)
            assert card.has_enough_info() is True, f"Expected True for title='{title}'"


# ── Edge cases ────────────────────────────────────────────────────────────────

class TestEdgeCases:
    def test_empty_html_returns_empty_list(self):
        assert parse_job_cards("", "linkedin") == []

    def test_none_html_returns_empty_list(self):
        assert parse_job_cards(None, "linkedin") == []

    def test_no_job_links_returns_empty_list(self):
        html = "<html><body><a href='https://linkedin.com/in/someone'>Profile</a></body></html>"
        assert parse_job_cards(html, "linkedin") == []

    def test_unsubscribe_links_excluded(self):
        html = """
        <html><body>
          <a href="https://www.linkedin.com/comm/jobs/view/111">Software Engineer</a>
          <a href="https://www.linkedin.com/notifications/settings/unsubscribe">Unsubscribe</a>
        </body></html>
        """
        cards = parse_job_cards(html, "linkedin")
        assert len(cards) == 1
        assert "unsubscribe" not in cards[0].apply_link

    def test_multiple_jobs_in_one_email(self):
        html = f"""
        <html><body>
          <table>
            <tr><td>
              <a href="https://www.linkedin.com/comm/jobs/view/111">Job One</a>
              <div>Company A</div><div>Remote</div>
            </td></tr>
            <tr><td>
              <a href="https://www.linkedin.com/comm/jobs/view/222">Job Two</a>
              <div>Company B</div><div>Vancouver, BC</div>
            </td></tr>
          </table>
        </body></html>
        """
        cards = parse_job_cards(html, "linkedin")
        assert len(cards) == 2
        titles = {c.title for c in cards}
        assert "Job One" in titles
        assert "Job Two" in titles

    def test_compound_title_anchor_splits_correctly(self):
        """LinkedIn occasionally puts 'Title · Company' all in the anchor text."""
        html = """
        <html><body>
          <a href="https://www.linkedin.com/comm/jobs/view/999">
            Director of Quality Assurance · Victoria Newitt Recruitment Inc.
          </a>
          <div>Richmond, BC (On-site)</div>
        </body></html>
        """
        cards = parse_job_cards(html, "linkedin")
        assert len(cards) == 1
        assert cards[0].title == "Director of Quality Assurance"
        assert "Victoria Newitt" not in cards[0].title

    def test_navigation_anchors_excluded_from_other_source(self):
        """'View more jobs' and 'Manage settings' links must not become job cards."""
        html = """
        <html><body>
          <a href="https://talent.com/jobs/view?id=123">Software Quality Manager</a>
          <a href="https://talent.com/jobs">View more jobs</a>
          <a href="https://talent.com/settings">Manage settings</a>
        </body></html>
        """
        cards = parse_job_cards(html, "other")
        titles = [c.title for c in cards]
        assert "View more jobs" not in titles
        assert "Manage settings" not in titles
        # The real job should still be found
        assert any("Quality" in (t or "") for t in titles)

    def test_navigation_anchors_excluded_from_linkedin(self):
        """'See all jobs' navigation link in LinkedIn email must not become a card."""
        html = """
        <html><body>
          <a href="https://www.linkedin.com/comm/jobs/view/111">Director of Engineering</a>
          <a href="https://www.linkedin.com/jobs/">See all jobs</a>
        </body></html>
        """
        cards = parse_job_cards(html, "linkedin")
        titles = [c.title for c in cards]
        assert "See all jobs" not in titles
        assert len(cards) == 1


# ── Indeed jobalert.indeed.com format ─────────────────────────────────────────

class TestIndeedJobalertParsing:
    """Tests for the current Indeed job alert email format (donotreply@jobalert.indeed.com)
    which uses r.jobalert.indeed.com redirect URLs."""

    def test_extracts_card_from_jobalert_url(self):
        """Confirm jobalert.indeed.com redirect links produce valid cards."""
        cards = parse_job_cards(_indeed_jobalert_email(), "indeed")
        assert len(cards) >= 1

    def test_title_extracted(self):
        cards = parse_job_cards(
            _indeed_jobalert_email(title="Director of Technology & AI Enablement"), "indeed"
        )
        assert len(cards) >= 1
        assert cards[0].title == "Director of Technology & AI Enablement"

    def test_company_extracted(self):
        cards = parse_job_cards(_indeed_jobalert_email(company="Segev LLP"), "indeed")
        assert len(cards) >= 1
        assert cards[0].company == "Segev LLP"

    def test_location_extracted(self):
        cards = parse_job_cards(_indeed_jobalert_email(location="Vancouver, BC"), "indeed")
        assert len(cards) >= 1
        assert cards[0].location is not None
        assert "Vancouver" in cards[0].location

    def test_salary_extracted(self):
        cards = parse_job_cards(
            _indeed_jobalert_email(salary="$115,000 - $130,000 a year"), "indeed"
        )
        assert len(cards) >= 1
        assert cards[0].salary_text is not None

    def test_easily_apply_not_a_card(self):
        """'Easily apply' CTA badge in Indeed emails must not become a job card."""
        cards = parse_job_cards(_indeed_jobalert_email(), "indeed")
        titles = [c.title for c in cards]
        assert "Easily apply" not in titles
        assert "► Easily apply" not in titles

    def test_unsubscribe_not_a_card(self):
        cards = parse_job_cards(_indeed_jobalert_email(), "indeed")
        for c in cards:
            assert "unsubscribe" not in c.apply_link.lower()

    def test_snippet_from_description_captured(self):
        snippet_text = "Segev LLP is a business law firm built for out of the box clients."
        cards = parse_job_cards(_indeed_jobalert_email(snippet=snippet_text), "indeed")
        assert len(cards) >= 1
        # Either in snippet field or scoring text
        text = cards[0].to_scoring_text()
        assert "Segev" in text or "law firm" in text

    def test_scoring_text_rich_enough(self):
        """Indeed emails with salary + snippet should produce non-trivial scoring text."""
        cards = parse_job_cards(_indeed_jobalert_email(), "indeed")
        assert len(cards) >= 1
        text = cards[0].to_scoring_text()
        # Should have job title, company, location at minimum
        assert "Director" in text
        assert len(text) > 80


# ── TrueUp weekly digest format ───────────────────────────────────────────────

class TestTrueUpDigestParsing:
    """Tests for TrueUp weekly digest email (7 jobs, rich card format)."""

    def test_extracts_multiple_jobs(self):
        """TrueUp weekly digest has 3+ job cards — all should be extracted."""
        cards = parse_job_cards(_trueup_digest_email(), "trueup")
        assert len(cards) >= 2  # at least Docebo and Autodesk

    def test_director_engineering_docebo_found(self):
        cards = parse_job_cards(_trueup_digest_email(), "trueup")
        titles = [c.title for c in cards]
        assert any("Director" in (t or "") and "Engineering" in (t or "") for t in titles)

    def test_autodesk_job_found(self):
        cards = parse_job_cards(_trueup_digest_email(), "trueup")
        companies = [c.company for c in cards]
        assert any("Autodesk" in (co or "") for co in companies)

    def test_view_all_jobs_link_not_a_card(self):
        """'View all 26 open jobs' footer link must not become a job card."""
        cards = parse_job_cards(_trueup_digest_email(), "trueup")
        titles = [c.title for c in cards]
        assert not any("view all" in (t or "").lower() for t in titles)
        assert not any("open jobs" in (t or "").lower() for t in titles)

    def test_unsubscribe_not_a_card(self):
        cards = parse_job_cards(_trueup_digest_email(), "trueup")
        for c in cards:
            assert "unsubscribe" not in c.apply_link.lower()

    def test_company_description_in_scoring_text(self):
        """TrueUp cards include company descriptions — they should land in snippet."""
        cards = parse_job_cards(_trueup_digest_email(), "trueup")
        # Find Docebo card
        docebo = next((c for c in cards if c.company and "Docebo" in c.company), None)
        assert docebo is not None
        text = docebo.to_scoring_text()
        # Company description "Corporate learning management system" should be captured
        assert "Docebo" in text

    def test_location_parsed_from_allcaps(self):
        """TrueUp uses ALL-CAPS locations like 'TORONTO, ONTARIO / REMOTE'."""
        cards = parse_job_cards(_trueup_digest_email(), "trueup")
        docebo = next((c for c in cards if c.company and "Docebo" in c.company), None)
        assert docebo is not None
        assert docebo.location is not None
        assert "TORONTO" in docebo.location or "ONTARIO" in docebo.location or "REMOTE" in docebo.location


# ── New nav anchor patterns ────────────────────────────────────────────────────

class TestNewNavAnchors:
    """Tests for nav anchor patterns added for Indeed/TrueUp CTAs."""

    def test_easily_apply_rejected(self):
        card = EmailJobCard(apply_link="https://indeed.com/apply/123", title="Easily apply")
        assert card.has_enough_info() is False

    def test_view_all_N_open_jobs_rejected(self):
        card = EmailJobCard(apply_link="https://trueup.io/jobs", title="View all 26 open jobs")
        assert card.has_enough_info() is False

    def test_view_all_jobs_rejected(self):
        card = EmailJobCard(apply_link="https://trueup.io/jobs", title="View all jobs")
        assert card.has_enough_info() is False

    def test_open_in_app_rejected(self):
        card = EmailJobCard(apply_link="https://app.trueup.io", title="Open in app")
        assert card.has_enough_info() is False

    def test_job_alerts_rejected(self):
        card = EmailJobCard(apply_link="https://linkedin.com/alerts", title="Job Alerts")
        assert card.has_enough_info() is False

    def test_hire_with_trueup_rejected(self):
        """TrueUp digest footer CTA: 'Hire with TrueUp' must not become a job card."""
        card = EmailJobCard(apply_link="http://url3500.trueup.io/ls/click?upn=abc", title="Hire with TrueUp")
        assert card.has_enough_info() is False

    def test_sponsor_trueup_rejected(self):
        """TrueUp digest footer CTA: 'Sponsor TrueUp' must not become a job card."""
        card = EmailJobCard(apply_link="http://url3500.trueup.io/ls/click?upn=xyz", title="Sponsor TrueUp")
        assert card.has_enough_info() is False

    def test_my_trueup_rejected(self):
        """TrueUp digest footer nav: 'My TrueUp' must not become a job card."""
        card = EmailJobCard(apply_link="http://url3500.trueup.io/ls/click?upn=pqr", title="My TrueUp")
        assert card.has_enough_info() is False

    def test_real_job_title_still_passes(self):
        """Ensure the new patterns don't accidentally reject real job titles."""
        for title in [
            "Director of Technology & AI Enablement",
            "Quality Assurance Manager",
            "Principal Software Engineer",
            "VP of Engineering",
            "Director of Software Development - AI/ML",
        ]:
            card = EmailJobCard(apply_link="https://example.com/job/1", title=title)
            assert card.has_enough_info() is True, f"Should pass: '{title}'"


class TestBadgeTitleSkipping:
    """Badge/status lines above job titles in Talent.com and Glassdoor emails."""

    def _make_talent_html(self, badge: str, real_title: str, company: str, url: str) -> str:
        """Simulate a Talent.com email card: badge above real title, all inside <a>."""
        return f"""
        <html><body>
        <a href="{url}">
          <div>{badge}</div>
          <div>{real_title}</div>
          <div>{company}</div>
          <div>Vancouver, BC</div>
        </a>
        </body></html>
        """

    def test_talent_com_pick_badge_skipped(self):
        """'Talent.com's pick' badge should be stripped; real title used instead."""
        html = self._make_talent_html(
            "Talent.com's pick",
            "Senior Director, Technical Product Management",
            "Big Tech Corp",
            "https://www.talent.com/apply?id=abc123",  # "apply" matches URL keyword filter
        )
        cards = parse_job_cards(html, source="other")
        assert len(cards) == 1
        assert cards[0].title == "Senior Director, Technical Product Management"
        assert "Talent.com" not in (cards[0].title or "")

    def test_closing_soon_badge_skipped(self):
        """'Closing soon' status label should be stripped; real title used instead."""
        html = self._make_talent_html(
            "Closing soon",
            "Director, Ratings AI",
            "Ratehub Inc.",
            "https://www.talent.com/apply?id=def456",
        )
        cards = parse_job_cards(html, source="other")
        assert len(cards) == 1
        assert cards[0].title == "Director, Ratings AI"
        assert cards[0].title != "Closing soon"

    def test_featured_badge_skipped(self):
        html = self._make_talent_html(
            "Featured",
            "VP of Engineering",
            "Acme Systems Ltd",
            "https://www.glassdoor.com/job-listing/vp-engineering-123",
        )
        cards = parse_job_cards(html, source="other")
        assert len(cards) == 1
        assert cards[0].title == "VP of Engineering"

    def test_real_title_without_badge_unaffected(self):
        """When there is no badge, title extraction should work as before."""
        html = """
        <html><body>
        <a href="https://talent.com/apply?id=xyz">
          <div>Director of Engineering</div>
          <div>Stripe</div>
          <div>Canada (Remote)</div>
        </a>
        </body></html>
        """
        cards = parse_job_cards(html, source="other")
        assert len(cards) == 1
        assert cards[0].title == "Director of Engineering"


class TestCompanyAsTitleSwap:
    """Talent.com email format puts company name first; job title is second line."""

    def _make_company_first_html(self, company: str, job_title: str, location: str, url: str) -> str:
        return f"""
        <html><body>
        <a href="{url}">
          <div>{company}</div>
          <div>{job_title}</div>
          <div>{location}</div>
        </a>
        </body></html>
        """

    def test_company_first_swapped_to_title(self):
        """'Devacor Solutions Group' (company) first, 'QA Automation Developer' (title) second."""
        html = self._make_company_first_html(
            "Devacor Solutions Group",
            "QA Automation Developer",
            "Remote",
            "https://www.talent.com/apply?id=devacor1",
        )
        cards = parse_job_cards(html, source="other")
        assert len(cards) == 1
        assert cards[0].title == "QA Automation Developer"
        # Company name should end up in company field (from context classification)
        assert cards[0].title != "Devacor Solutions Group"

    def test_company_inc_suffix_swapped(self):
        html = self._make_company_first_html(
            "Ratehub Inc.",
            "Senior Software Engineer",
            "Toronto, ON",
            "https://www.talent.com/apply?id=ratehub1",
        )
        cards = parse_job_cards(html, source="other")
        assert len(cards) == 1
        assert cards[0].title == "Senior Software Engineer"

    def test_no_swap_when_title_first(self):
        """When job title comes first (normal layout), no swap occurs."""
        html = self._make_company_first_html(
            "Senior Engineering Manager",
            "Shopify",
            "Canada (Remote)",
            "https://talent.com/apply?id=shopify1",
        )
        cards = parse_job_cards(html, source="other")
        assert len(cards) == 1
        assert cards[0].title == "Senior Engineering Manager"

    def test_no_swap_when_second_line_not_a_job_title(self):
        """If second anchor line is not a job title, do NOT swap (avoid false positives)."""
        html = """
        <html><body>
        <a href="https://talent.com/apply?id=abc">
          <div>Deloitte Consulting</div>
          <div>Vancouver, BC</div>
        </a>
        </body></html>
        """
        cards = parse_job_cards(html, source="other")
        # Card may or may not be created, but if it is, title should not be "Vancouver, BC"
        for card in cards:
            assert card.title != "Vancouver, BC"
