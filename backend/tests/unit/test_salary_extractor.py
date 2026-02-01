"""Unit tests for app.utils.salary_extractor -- structured salary parsing."""

import pytest
from app.utils.salary_extractor import extract_salary_info, extract_salary, SalaryInfo


class TestExtractSalaryInfo:
    def test_annual_range(self):
        text = "The range for base pay is $140,000 - $200,000 per year"
        info = extract_salary_info(text)
        assert info is not None
        assert info.min_amount is not None
        assert info.max_amount is not None
        assert info.min_amount <= info.max_amount

    def test_k_suffix_range(self):
        text = "Compensation: $120K-$150K annually"
        info = extract_salary_info(text)
        assert info is not None
        assert info.min_amount == 120000
        assert info.max_amount == 150000
        assert info.frequency == "annual"

    def test_hourly_rate(self):
        text = "Pay range: $25-35 per hour"
        info = extract_salary_info(text)
        assert info is not None
        assert info.frequency == "hourly"

    def test_cad_currency(self):
        text = "The full salary range for this role is $158,900 to $198,600 to $238,300 CAD"
        info = extract_salary_info(text)
        assert info is not None
        assert info.currency == "CAD"
        assert info.min_amount == 158900
        assert info.max_amount == 238300

    def test_no_salary_returns_none(self):
        text = "Great opportunity to work with a talented team."
        assert extract_salary_info(text) is None

    def test_empty_returns_none(self):
        assert extract_salary_info("") is None
        assert extract_salary_info(None) is None

    def test_monthly_frequency(self):
        text = "Salary: $4000-$6000 monthly"
        info = extract_salary_info(text)
        assert info is not None
        assert info.frequency == "monthly"

    def test_weekly_frequency(self):
        text = "The salary is ranging from $800 to $950 weekly"
        info = extract_salary_info(text)
        assert info is not None
        assert info.frequency == "weekly"

    def test_biweekly_frequency(self):
        text = "The salary is ranging from $12,000 to $15,000 bi-weekly"
        info = extract_salary_info(text)
        assert info is not None
        assert info.frequency == "bi-weekly"
        assert info.min_amount == 12000
        assert info.max_amount == 15000

    def test_starting_at_single_amount(self):
        text = "Starting at $90K per year"
        info = extract_salary_info(text)
        assert info is not None
        assert info.min_amount == 90000
        assert info.frequency == "annual"

    def test_unrealistic_hourly_filtered(self):
        # $1/hr is below the $5 minimum for hourly
        text = "Pay: $1/hour"
        info = extract_salary_info(text)
        # Should be None because amount is unrealistic
        assert info is None


class TestSalaryInfoAttributes:
    def test_has_required_attributes(self):
        info = SalaryInfo(raw_text="$100K", min_amount=100000, max_amount=100000)
        assert hasattr(info, "raw_text")
        assert hasattr(info, "min_amount")
        assert hasattr(info, "max_amount")
        assert hasattr(info, "currency")
        assert hasattr(info, "frequency")

    def test_defaults(self):
        info = SalaryInfo(raw_text="test")
        assert info.currency == "USD"
        assert info.frequency == "annual"
        assert info.min_amount is None
        assert info.max_amount is None

    def test_str_returns_raw_text(self):
        info = SalaryInfo(raw_text="$120K-$150K")
        assert str(info) == "$120K-$150K"


class TestExtractSalaryBackwardCompat:
    def test_returns_string_when_found(self):
        text = "Salary: $100,000 - $150,000 per year"
        result = extract_salary(text)
        assert isinstance(result, str)
        assert "$" in result

    def test_returns_none_when_not_found(self):
        result = extract_salary("No salary mentioned here.")
        assert result is None
