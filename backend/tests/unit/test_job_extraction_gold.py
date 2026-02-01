# File: //backend/tests/unit/test_job_extraction_gold.py

import csv
from pathlib import Path
import re

from app.utils.job_extraction import (
    extract_title,
    extract_company_name,
    extract_location,
    extract_salary,
)

FIXTURE = Path(__file__).parent / "gold_jobs_new.csv"

def norm(s: str) -> str:
    return (s or "").strip().lower()

def norm_title(s: str) -> str:
    s = (s or "").strip().lower()
    s = re.sub(r"\s+", " ", s)
    # remove prefixes like "job title:"
    s = re.sub(r"^(job title|title|position|role)\s*:\s*", "", s)
    # drop suffix after dash or pipe
    s = re.split(r"\s+[–—-]\s+", s, maxsplit=1)[0]
    s = s.split("|", 1)[0]
    return s.strip()


def test_gold_extraction_report():
    rows = []
    with FIXTURE.open("r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    total = len(rows)
    assert total > 0

    hit = {"title": 0, "company": 0, "location": 0, "salary": 0}
    present = {"salary": 0, "location": 0}

    failures = []

    for r in rows:
        jd = r["job_description"] or ""
        truth_title = r["job_title"] or ""
        truth_company = r["company_name"] or ""
        truth_loc = r["location"] or ""
        truth_salary = (r["salary"] or "").strip()

        pred_title = extract_title(jd)
        pred_company = extract_company_name(jd)
        pred_loc = extract_location(jd)
        pred_salary = extract_salary(jd)
        
        if norm_title(pred_title) == norm_title(truth_title):
            hit["title"] += 1
        else:
            failures.append(("title", r["id"], truth_title, pred_title))

        if norm(pred_company) == norm(truth_company):
            hit["company"] += 1
        else:
            failures.append(("company", r["id"], truth_company, pred_company))

        # Location/salary: score accuracy only when JD likely contains it
        # (optional: later we improve presence detection)
        if truth_loc.strip():
            present["location"] += 1
            if norm(pred_loc) == norm(truth_loc):
                hit["location"] += 1
            else:
                failures.append(("location", r["id"], truth_loc, pred_loc))

        if truth_salary:
            present["salary"] += 1
            if norm(pred_salary) == norm(truth_salary):
                hit["salary"] += 1
            else:
                failures.append(("salary", r["id"], truth_salary, pred_salary))

    title_acc = hit["title"] / total
    company_acc = hit["company"] / total
    loc_acc = hit["location"] / max(1, present["location"])
    sal_acc = hit["salary"] / max(1, present["salary"])

    print("\n=== GOLD EXTRACTION REPORT ===")
    print(f"Rows: {total}")
    print(f"Title accuracy:    {title_acc:.2%}")
    print(f"Company accuracy:  {company_acc:.2%}")
    print(f"Location accuracy: {loc_acc:.2%}  (only when present)")
    print(f"Salary accuracy:   {sal_acc:.2%}  (only when present)")
    print("\nTop failures (first 60):")
    for f in failures[:]:
        print(f)

    # Don’t hard-fail yet—first run is to establish baseline.
    # Later we’ll lock thresholds like:
    # assert title_acc >= 0.80
