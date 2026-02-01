import pandas as pd
import re

def engine_extract(text, known_companies=None):
    if not isinstance(text, str): return "Not found", "Not found"
    
    # --- 1. TITLE EXTRACTION (V3 High-Accuracy Logic) ---
    found_title = "Not found"
    
    # Priority A: Headers
    headers = [r"(?i)Job Title[:\-]\s*(.*)", r"(?i)Position[:\-]\s*(.*)", r"(?i)Role[:\-]\s*(.*)"]
    for p in headers:
        match = re.search(p, text)
        if match:
            t = match.group(1).split('\n')[0].strip()
            if len(t) > 3: 
                found_title = t
                break
            
    # Priority B: Phrases
    if found_title == "Not found":
        phrases = [
            r"(?i)looking for a[n]?\s+([^,.]+?)\s+to\s+",
            r"(?i)looking for a[n]?\s+([^,.]+?)\s+at\s+",
            r"(?i)seeking a[n]?\s+([^,.]+?)\s+to\s+",
            r"(?i)join (?:us|our team) as a[n]?\s+([^,.]+?)(?:\s+at|\s+to|\n|\.)",
            r"(?i)as a[n]?\s+([^,.]+?)\s+at\s+",
        ]
        for p in phrases:
            match = re.search(p, text)
            if match:
                t = match.group(1).strip()
                t = re.sub(r"(?i)^(experienced|visionary|dynamic|talented|seasoned|successful|highly motivated)\s+", "", t)
                if 5 < len(t) < 80: 
                    found_title = t
                    break

    # Priority C: Keyword Scorer (Optimized Parameters)
    if found_title == "Not found":
        keywords = ["Director", "Manager", "Engineer", "Lead", "VP", "Head of", "Architect", "Principal", "Specialist"]
        lines = [l.strip() for l in text.split('\n') if l.strip()]
        best_candidate, max_score = "Not found", 0
        
        for i, line in enumerate(lines[:30]): # Scans deeper (30 lines)
            score = 0
            if any(kw in line for kw in keywords): score += 10
            if len(line) < 60: score += 5
            if line[0].isupper(): score += 5
            
            # Penalties
            if any(x in line.lower() for x in ["about the job", "welcome", "is a", "is the", "click", "apply"]):
                score -= 20
            
            # Distance decay (Gentler penalty)
            score -= (i * 0.5)
            
            if score > max_score:
                max_score, best_candidate = score, line
                
        if max_score > 10:
            found_title = best_candidate

    # --- 2. COMPANY EXTRACTION (V4 Robust Logic) ---
    found_company = "Not found"
    
    # A. "About [Company]" with Blacklist to avoid "the job"
    blacklist = ["the job", "the company", "the role", "us", "our company", "you", "the team"]
    about_match = re.search(r"(?i)(?:About|More About)\s+([A-Z][\w\s&]+?)(?:\s+is|\n|:)", text)
    if about_match:
        cand = about_match.group(1).strip()
        if cand.lower() not in blacklist:
            found_company = cand

    # B. Intro check: "[Company] is/pioneers/helps..."
    if found_company == "Not found":
        clean = re.sub(r"(?i)^About the job\s*", "", text).strip()
        is_match = re.search(r"^([A-Z][\w\s&]{2,30}?)\s+(?:is|empowers|pioneers|provides|builds|helps|unites|makes)", clean)
        if is_match:
            cand = is_match.group(1).strip()
            if cand.lower() not in ["this", "it", "we", "you"]:
                found_company = cand

    # C. Dictionary Lookup (Safely check known_companies)
    if found_company == "Not found" and known_companies is not None:
        for co in sorted(list(known_companies), key=len, reverse=True):
            if isinstance(co, str) and len(co) > 2:
                if re.search(r'\b' + re.escape(co) + r'\b', text[:1200]):
                    found_company = co
                    break
                
    return found_title, found_company

# --- TEST ON YOUR DATAFRAME ---
# results = df['job_description'].apply(lambda x: engine_extract_robust(x, known_cos))
# --- EVALUATION ---
df = pd.read_csv('gold_jobs_with_snippets.csv')
known_cos = df['company_name'].dropna().unique()

results = df['job_description'].apply(lambda x: engine_extract(x, known_cos))
df['pred_title'], df['pred_company'] = [r[0] for r in results], [r[1] for r in results]

# Scoring Logic (Fuzzy match)
df['title_ok'] = df.apply(lambda r: r['job_title'].lower() in r['pred_title'].lower() or r['pred_title'].lower() in r['job_title'].lower(), axis=1)
df['company_ok'] = df.apply(lambda r: r['company_name'].lower() in r['pred_company'].lower() or r['pred_company'].lower() in r['company_name'].lower(), axis=1)

print(f"Final Title Accuracy: {df['title_ok'].mean():.1%}")
print(f"Final Company Accuracy: {df['company_ok'].mean():.1%}")
df.to_csv('extraction_engine_results.csv', index=False)