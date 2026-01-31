import csv
import re
import os
import pandas as pd
from pathlib import Path
from app.utils.job_extraction import extract_title, extract_company_name

# Force the path to be relative to this script
BASE_DIR = Path(__file__).parent
FIXTURE = BASE_DIR / "gold_jobs_latest.csv"
OUT_CSV = BASE_DIR / "extraction_results_debug.csv"

def norm(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").strip()).lower()

def norm_title(s: str) -> str:
    s = norm(s)
    s = re.sub(r"^(job title|title|position|role)\s*:\s*", "", s)
    s = re.split(r"\s+[–—-]\s+", s, maxsplit=1)[0]
    return s.split("|", 1)[0].strip()

def test_gold_report():
    if not FIXTURE.exists():
        print(f"FAILED: Cannot find {FIXTURE.absolute()}")
        return

    df_helper = pd.read_csv(FIXTURE)
    known_cos = df_helper['company_name'].dropna().unique().tolist()
    rows = df_helper.to_dict('records')

    total = len(rows)
    title_hit, company_hit = 0, 0
    debug_data = []

    for r in rows:
        jd = str(r.get("job_description") or "")
        job_id = r.get("id") or "?"
        
        truth_t_raw = str(r.get("job_title") or "")
        truth_c_raw = str(r.get("company_name") or "")

        # Extraction
        pred_t_raw = extract_title(jd)
        pred_c_raw = extract_company_name(jd, known_cos)

        # Accuracy Check (Fuzzy match)
        t_match = norm_title(truth_t_raw) in norm_title(pred_t_raw) or norm_title(pred_t_raw) in norm_title(truth_t_raw)
        c_match = norm(truth_c_raw) in norm(pred_c_raw) or norm(pred_c_raw) in norm(truth_c_raw)

        if t_match: title_hit += 1
        if c_match: company_hit += 1

        debug_data.append({
            "ID": job_id,
            "Truth_Title": truth_t_raw,
            "Pred_Title": pred_t_raw,
            "T_Match": t_match,
            "Truth_Company": truth_c_raw,
            "Pred_Company": pred_c_raw,
            "C_Match": c_match
        })

    # Save and Confirm
    pd.DataFrame(debug_data).to_csv(OUT_CSV, index=False)
    
    print("\n=== GOLD ACCURACY REPORT ===")
    print(f"File: {FIXTURE.name}")
    print(f"Title Accuracy:   {title_hit}/{total} ({(title_hit/total):.2%})")
    print(f"Company Accuracy: {company_hit}/{total} ({(company_hit/total):.2%})")
    print(f"\nDEBUG CSV SAVED TO: {OUT_CSV.absolute()}")

    print("\n--- Top Title Failures ---")
    df_db = pd.DataFrame(debug_data)
    for _, row in df_db[df_db["T_Match"] == False].head(8).iterrows():
        print(f"ID {row['ID']} | Truth: {row['Truth_Title'][:80]} | Pred: {row['Pred_Title']}")

if __name__ == "__main__":
    test_gold_report()