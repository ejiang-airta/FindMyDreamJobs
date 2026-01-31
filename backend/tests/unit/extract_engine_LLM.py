

import google.generativeai as genai
import json
import pandas as pd

# Setup
genai.configure(api_key="AIzaSyAJez6VhVVMyVPqzlItTRxgl7Lleia1GKE")
model = genai.GenerativeModel('gemini-3-flash-preview')

def engine_extract(text, known_companies=None):
    if not isinstance(text, str) or len(text.strip()) < 10:
        return "Not found", "Not found"

    # FIXED: Safe check for numpy arrays / lists
    co_context = ""
    if known_companies is not None and len(known_companies) > 0:
        # Convert to list and take first 30
        co_list = list(known_companies)[:30]
        co_context = f"Likely candidate companies include: {co_list}"

    prompt = f"""
    You are a professional recruiter. Extract the 'job_title' and 'company_name' 
    from the job description provided below.
    
    Rules:
    1. Return ONLY valid JSON.
    2. If info is missing, use 'Not found'.
    
    {co_context}
    
    Text: 
    {text[:2000]}
    """

    try:
        response = model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"}
        )
        
        data = json.loads(response.text)
        return data.get('job_title', 'Not found'), data.get('company_name', 'Not found')
    except Exception as e:
        # It's helpful to see the error during testing
        print(f"LLM Error: {e}")
        return "Error", "Error"
    
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