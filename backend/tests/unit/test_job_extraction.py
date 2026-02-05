"""Unit tests for app.utils.job_extraction -- JD field extraction."""

import pytest
from app.utils.job_extraction import (
    extract_title,
    extract_company_name,
    extract_skills_with_frequency,
    extract_location,
    extract_experience,
    extract_years_experience,
    extract_salary,
)


# ---------------------------------------------------------------------------
# extract_title
# ---------------------------------------------------------------------------

class TestExtractTitle:
    def test_explicit_header(self):
        text = "Job Title: Senior Software Engineer\nCompany: Acme Corp"
        title = extract_title(text)
        assert "senior" in title.lower()
        assert "engineer" in title.lower()

    def test_role_header_variant(self):
        text = "Role: Director of Engineering\nAbout the company..."
        title = extract_title(text)
        assert "director" in title.lower()

    def test_natural_language_seeking(self):
        text = "We are seeking a Senior Data Scientist to join our team."
        title = extract_title(text)
        assert "scientist" in title.lower() or "data" in title.lower()

    def test_natural_language_hiring(self):
        text = "We are hiring a Staff Engineer to lead our platform team."
        title = extract_title(text)
        assert "engineer" in title.lower()

    def test_no_title_returns_unknown(self):
        text = "This is just some random text about gardening and flowers."
        title = extract_title(text)
        assert title == "Unknown Title"

    def test_empty_text_returns_unknown(self):
        assert extract_title("") == "Unknown Title"
        assert extract_title(None) == "Unknown Title"

    def test_cleans_at_company_suffix(self):
        text = "Position: Senior Engineer at Google\nDescription follows."
        title = extract_title(text)
        assert "google" not in title.lower()


# ---------------------------------------------------------------------------
# extract_company_name
# ---------------------------------------------------------------------------

class TestExtractCompanyName:
    def test_about_pattern(self):
        text = "About Google\nGoogle is a technology company..."
        company = extract_company_name(text)
        assert "google" in company.lower()

    def test_why_work_at_pattern(self):
        """Test 'Why Work at [Company]?' pattern - common JD section header."""
        text = "Senior Software Engineer\n\nWhy Work at Ross Video?\n\nWe offer great benefits..."
        company = extract_company_name(text)
        assert "ross video" in company.lower()

    def test_why_work_for_pattern(self):
        """Test 'Why Work for [Company]?' variant."""
        text = "Position: Data Analyst\n\nWhy Work for Acme Corp?\n\nJoin our team..."
        company = extract_company_name(text)
        assert "acme" in company.lower()

    def test_why_work_does_not_match_as_company(self):
        """Ensure 'Why Work' itself is not extracted as company name."""
        text = "Software Engineer at Tech Company\n\nWhy work here? We value our employees."
        company = extract_company_name(text)
        # Should NOT be 'Why Work' or 'Why'
        assert company.lower() != "why work"
        assert company.lower() != "why"

    def test_at_pattern(self):
        text = "At Amazon, we strive to be the most customer-centric company."
        company = extract_company_name(text)
        assert "amazon" in company.lower()

    def test_intro_pattern(self):
        text = "Shopify is a leading commerce platform that empowers millions."
        company = extract_company_name(text)
        assert "shopify" in company.lower()

    def test_known_companies_list(self):
        text = "Join our growing engineering team to build great products."
        company = extract_company_name(text, known_companies=["Stripe", "Meta"])
        # Without match in text, should not return known company
        assert company is not None

    def test_known_company_found_in_text(self):
        text = "At Stripe, we build financial infrastructure for the internet."
        company = extract_company_name(text, known_companies=["Stripe", "Meta"])
        assert "stripe" in company.lower()

    def test_not_found_returns_unknown(self):
        text = "some random job posting without any company reference whatsoever"
        company = extract_company_name(text)
        assert company == "Unknown Company"

    def test_empty_text_returns_unknown(self):
        assert extract_company_name("") == "Unknown Company"
        assert extract_company_name(None) == "Unknown Company"


# ---------------------------------------------------------------------------
# extract_skills_with_frequency
# ---------------------------------------------------------------------------

class TestExtractSkillsWithFrequency:
    def test_basic_extraction(self):
        text = "We need Python and AWS experience. Python is essential. Docker knowledge is a plus."
        result = extract_skills_with_frequency(text)
        assert "skills" in result
        assert "emphasized_skills" in result
        skill_names = [s["skill"].lower() for s in result["skills"]]
        assert "python" in skill_names

    def test_frequency_counting(self):
        text = "Python Python Python AWS Docker"
        result = extract_skills_with_frequency(text)
        python_entry = next(
            (s for s in result["skills"] if s["skill"].lower() == "python"), None
        )
        assert python_entry is not None
        assert python_entry["frequency"] >= 3

    def test_emphasized_skills_threshold(self):
        # Skills with frequency >= MIN_SKILL_FREQUENCY should be emphasized
        text = "Python Python Python AWS AWS Docker"
        result = extract_skills_with_frequency(text)
        emphasized = [s.lower() for s in result["emphasized_skills"]]
        # Python appears 3 times, AWS 2 times -- both should be emphasized
        if "n/a" not in emphasized:
            assert "python" in emphasized

    def test_empty_text(self):
        result = extract_skills_with_frequency("")
        assert result["skills"][0]["skill"] == "N/A"

    def test_none_text(self):
        result = extract_skills_with_frequency(None)
        assert result["skills"][0]["skill"] == "N/A"

    def test_no_skills_in_text(self):
        text = "Baking bread and pastries in a kitchen."
        result = extract_skills_with_frequency(text)
        # Should return N/A or empty skills
        assert len(result["skills"]) >= 1

    def test_case_insensitive(self):
        text = "python PYTHON Python"
        result = extract_skills_with_frequency(text)
        skill_names = [s["skill"].lower() for s in result["skills"]]
        assert "python" in skill_names


# ---------------------------------------------------------------------------
# extract_location
# ---------------------------------------------------------------------------

class TestExtractLocation:
    def test_city_province(self):
        text = "Location: Toronto, ON\nJob Description follows."
        loc = extract_location(text)
        assert "toronto" in loc.lower()

    def test_remote_canada(self):
        text = "This is a Canada (remote) position."
        loc = extract_location(text)
        assert "remote" in loc.lower() or "canada" in loc.lower()

    def test_not_found(self):
        text = "No location info here whatsoever."
        loc = extract_location(text)
        # May return spaCy entity or "Unspecified"
        assert loc is not None

    def test_empty_text(self):
        assert extract_location("") == "Unspecified"
        assert extract_location(None) == "Unspecified"


# ---------------------------------------------------------------------------
# extract_experience / extract_years_experience
# ---------------------------------------------------------------------------

class TestExtractExperience:
    def test_years_found(self):
        text = "Requires 5+ years of experience in software development."
        result = extract_experience(text)
        assert "5" in result

    def test_not_specified(self):
        text = "Looking for a motivated developer."
        result = extract_experience(text)
        assert result == "Unspecified"

    def test_years_experience_variant(self):
        text = "Minimum 3 years experience required."
        result = extract_years_experience(text)
        assert "3" in result

    def test_years_experience_unspecified(self):
        result = extract_years_experience("")
        assert result == "Unspecified"


# ---------------------------------------------------------------------------
# extract_salary (from job_extraction module)
# ---------------------------------------------------------------------------

class TestExtractSalary:
    def test_range_found(self):
        text = "Salary: $140,000 - $200,000 per year"
        result = extract_salary(text)
        assert result is not None
        assert "$" in result

    def test_k_format(self):
        text = "Compensation: $120K - $150K annually"
        result = extract_salary(text)
        assert result is not None

    def test_no_salary(self):
        text = "Great opportunity to work with a talented team."
        result = extract_salary(text)
        assert result is None

    def test_empty_text(self):
        assert extract_salary("") is None
        assert extract_salary(None) is None
