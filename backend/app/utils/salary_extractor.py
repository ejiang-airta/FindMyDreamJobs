# Utility for extracting structured salary information from job descriptions
# File: backend/app/utils/salary_extractor.py
import re
from typing import Optional, Dict, Tuple

class SalaryInfo:
    """Structured salary information"""
    def __init__(self, raw_text: str, min_amount: Optional[float] = None,
                 max_amount: Optional[float] = None, currency: str = "USD",
                 frequency: str = "annual"):
        self.raw_text = raw_text
        self.min_amount = min_amount
        self.max_amount = max_amount
        self.currency = currency
        self.frequency = frequency  # annual, hourly, weekly, bi-weekly, monthly

    def __str__(self):
        return self.raw_text

def extract_salary_info(job_description: str) -> Optional[SalaryInfo]:
    """
    Extract comprehensive salary information from job descriptions.
    Returns SalaryInfo object with parsed details or None if no salary found.
    """
    if not job_description:
        return None

    # Comprehensive salary patterns - ordered by specificity
    # IMPORTANT: each pattern must be a separate element (comma-separated)
    patterns = [
        # CAD/USD pay range: "The pay range for this role is: 140,000 - 200,000 CAD per year"
        r'(?:pay range for this role is[:\s]*)?(\d{1,3}(?:,\d{3})*)\s*[-–—]\s*(\d{1,3}(?:,\d{3})*)\s*(CAD|USD)\s*(?:per year|annually)?',

        # Compensation/Salary with K-suffix range: "$120K-$150K annually"
        r'(?:compensation|salary|pay)\s*:\s*\$(\d+)\s*K\s*[-–—]\s*\$?\s*(\d+)\s*K\s*(?:annually|per year|/year)?',

        # Generic K-suffix ranges: "$120K-$150K", "$120K - $150K annually"
        r'\$\s?(\d{1,3})\s*K\s*[-–—]\s*\$?\s?(\d{1,3})\s*K(?:\s*(?:annually|per year|/year))?',

        # Starting at with K: "Starting at $90K per year"
        r'(?:starting)\s+at\s+\$(\d+)\s*K\s*(?:per year|annually|/year)?',

        # Salary keyword with range and K suffix: "Salary: 140-150K"
        r'(?:salary|compensation|pay|wage)\s*:\s*(\d{1,3})\s*[-–—]\s*(\d{1,3})\s*K',

        # Salary with dollar range and frequency: "Salary: $4000-$6000 monthly"
        r'(?:salary|pay|compensation)\s*:\s*\$(\d+(?:,\d{3})*(?:\.\d{2})?)\s*[-–—]\s*\$?\s*(\d+(?:,\d{3})*(?:\.\d{2})?)\s*(monthly|weekly|bi-weekly|hourly|per hour|per week)',

        # Hourly rates with range
        r'(?:hourly rate|rate).*?(?:starts)?\s*(?:at\s*)?'
        r'\$\s?(\d{1,3}(?:\.\d{2})?)\s*/hour\s*(?:to)\s*'
        r'\$\s?(\d{1,3}(?:\.\d{2})?)\s*/hour',

        # Pay range: $X-Y per hour (without $ on second number)
        r'(?:pay range)\s*:\s*'
        r'\$\s?(\d{1,3}(?:\.\d{2})?)\s*[-–—]\s*'
        r'(\d{1,3}(?:\.\d{2})?)\s*(?:per hour|/hour|/hr)',

        # Weekly/Bi-weekly patterns with range — MUST be before generic "to" patterns
        r'(?:salary|pay).*?(?:ranging\s*)?(?:from\s*)?'
        r'\$\s?(\d+(?:,\d{3})*(?:\.\d{2})?)\s*(?:[-–—]|to)\s*'
        r'\$?\s?(\d+(?:,\d{3})*(?:\.\d{2})?)\s*'
        r'(bi-weekly|weekly|per week)',

        # Complex ranges with multiple amounts and currency
        r'(?:salary|pay|compensation).*?(?:range|is).*?'
        r'\$\s?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)\s*(?:to)\s*'
        r'\$\s?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)\s*(?:to\s*'
        r'\$\s?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?))?\s*(?:CAD|USD)?',

        # Standard ranges with dash/hyphen
        r'(?:salary|pay|compensation|range|base pay).*?'
        r'\$\s?(\d+(?:,\d{3})*(?:\.\d{2})?)\s*[-–—]\s*'
        r'\$?\s?(\d+(?:,\d{3})*(?:\.\d{2})?)',

        # Ranges with "to" or "up to"
        r'(?:salary|pay|compensation).*?(?:from|at)?\s*'
        r'\$\s?(\d+(?:,\d{3})*(?:\.\d{2})?)\s*(?:to|up to)\s*'
        r'\$?\s?(\d+(?:,\d{3})*(?:\.\d{2})?)',

        # Single K format amounts with keyword
        r'(?:starting|salary|pay|compensation).*?(?:at\s*)?'
        r'\$\s?(\d{1,3})\s*K(?:\s*(?:per year|annually|/year))?',

        # Single amounts with frequency
        r'(?:salary|pay|compensation|base salary).*?(?:starts|is)?.*?(?:at\s*)?'
        r'\$\s?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)\s*'
        r'(per year|annually|/year|/hr|/hour|hourly|weekly|bi-weekly|per week|monthly)',

        # Fallback: any dollar amount with commas
        r'\$\s?(\d{1,3}(?:,\d{3})+(?:\.\d{2})?)',
    ]

    for pattern in patterns:
        matches = re.finditer(pattern, job_description, re.IGNORECASE | re.MULTILINE)

        for match in matches:
            salary_info = _parse_salary_match(match, job_description)
            if salary_info:
                return salary_info

    return None

def _parse_salary_match(match, job_description: str) -> Optional[SalaryInfo]:
    """Parse a regex match into structured salary information"""
    groups = match.groups()
    full_match = match.group(0)

    # Clean and extract amounts
    amounts = []
    frequency = "annual"  # default
    currency = "USD"  # default

    # Check if the pattern was a K-suffix pattern (amounts need *1000)
    is_k_pattern = bool(re.search(r'\$\d+\s*K', full_match, re.IGNORECASE))

    # Extract numeric values and frequency indicators
    for group in groups:
        if group is None:
            continue
        if re.search(r'\d', group):
            # Handle regular numbers
            clean_num = re.sub(r'[^\d.]', '', group)
            if clean_num:
                try:
                    num_val = float(clean_num)
                    # If this is a K-suffix pattern match, multiply small numbers by 1000
                    if is_k_pattern and num_val < 1000:
                        num_val *= 1000
                    amounts.append(num_val)
                except ValueError:
                    continue
        else:
            # Check for frequency indicators in non-numeric groups
            group_lower = group.lower()
            if any(term in group_lower for term in ['hour', 'hr']):
                frequency = "hourly"
            elif 'bi-weekly' in group_lower:
                frequency = "bi-weekly"
            elif 'weekly' in group_lower or 'per week' in group_lower:
                frequency = "weekly"
            elif 'month' in group_lower:
                frequency = "monthly"
            elif any(term in group_lower for term in ['annually', 'per year', '/year']):
                frequency = "annual"

    # Additional frequency detection from full match
    full_match_lower = full_match.lower()
    if any(term in full_match_lower for term in ['hour', '/hr']) and frequency == "annual":
        frequency = "hourly"
    elif 'bi-weekly' in full_match_lower and frequency == "annual":
        frequency = "bi-weekly"
    elif ('weekly' in full_match_lower or 'per week' in full_match_lower) and 'bi' not in full_match_lower and frequency == "annual":
        frequency = "weekly"
    elif 'month' in full_match_lower and frequency == "annual":
        frequency = "monthly"

    # Currency detection — check full match AND surrounding context (next 10 chars after match)
    match_end = match.end()
    context_after = job_description[match_end:match_end + 15].upper()
    if 'CAD' in full_match.upper() or 'CAD' in context_after:
        currency = "CAD"

    # Filter out unrealistic amounts based on frequency
    amounts = _filter_realistic_amounts(amounts, frequency)

    if not amounts:
        return None

    # Sort amounts to get min/max
    amounts.sort()

    return SalaryInfo(
        raw_text=full_match.strip(),
        min_amount=amounts[0] if amounts else None,
        max_amount=amounts[-1] if len(amounts) > 1 else amounts[0] if amounts else None,
        currency=currency,
        frequency=frequency
    )

def _filter_realistic_amounts(amounts: list, frequency: str) -> list:
    """Filter out unrealistic salary amounts based on frequency"""
    filtered = []

    for amount in amounts:
        if frequency == "hourly":
            # Hourly: $5-500/hour reasonable
            if 5 <= amount <= 500:
                filtered.append(amount)
        elif frequency == "weekly":
            # Weekly: $200-10000/week reasonable
            if 200 <= amount <= 10000:
                filtered.append(amount)
        elif frequency == "bi-weekly":
            # Bi-weekly: $400-50000 reasonable (covers high earners)
            if 400 <= amount <= 50000:
                filtered.append(amount)
        elif frequency == "monthly":
            # Monthly: $1000-100000/month reasonable
            if 1000 <= amount <= 100000:
                filtered.append(amount)
        else:  # annual
            # Annual: $15000-2000000 reasonable
            if 15000 <= amount <= 2000000:
                filtered.append(amount)

    return filtered

def extract_salary(job_description: str) -> Optional[str]:
    """
    Backward compatible function that returns raw salary text.
    Use extract_salary_info() for structured data.
    """
    salary_info = extract_salary_info(job_description)
    return salary_info.raw_text if salary_info else None

# Test the function with your examples
if __name__ == "__main__":
    test_cases = [
        "The full salary range* for this role is $158,900 to $198,600 to $238,300 CAD",
        "The range for base pay is $140,000 - $200,000 which is dependent on level of experience",
        "The base salary starts at $80,000 up to $140,000 per year",
        "The salary is ranging from $12,000 to $15,000 bi-weekly",
        "The salary is ranging from $800 to $950 weekly",
        "The hourly rate starts at $34/hour to $45/hour",
        "Compensation: $120K-$150K annually",
        "Pay range: $25-35 per hour",
        "Starting at $90K per year",
        "Salary: $4000-$6000 monthly"
    ]

    print("Testing salary extraction:")
    print("=" * 50)

    for i, case in enumerate(test_cases, 1):
        result = extract_salary_info(case)
        print(f"{i}. Input: {case}")
        if result:
            print(f"   Raw: {result.raw_text}")
            print(f"   Range: ${result.min_amount:,.0f} - ${result.max_amount:,.0f}" if result.min_amount and result.max_amount and result.min_amount != result.max_amount else f"   Amount: ${result.min_amount:,.0f}" if result.min_amount else "   Amount: N/A")
            print(f"   Frequency: {result.frequency}, Currency: {result.currency}")
        else:
            print("   No salary found")
        print()
