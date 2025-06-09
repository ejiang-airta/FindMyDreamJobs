# File: backend/app/routes/job_search.py

from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
import requests
import os
from app.utils.salary_extractor import extract_salary


router = APIRouter()

# RapidAPI instance
rapid_api_host = 'jsearch.p.rapidapi.com'
rapid_api_key = os.getenv("RAPIDAPI_KEY")
API_URL = f"https://{rapid_api_host}/search"    #jsearch API URL

@router.get("/search-jobs")
def search_jobs(query: str = Query(..., description="Search keyword for jobs")):
    try:
         # jsearch API
        headers = {
            'x-rapidapi-host': rapid_api_host.encode("ascii", "ignore").decode(),
            'x-rapidapi-key': rapid_api_key.encode("ascii", "ignore").decode()
            }
        # API parameters
        params = {
                "query": query,
                "page":"1",
                "num_pages":"4",
                "country":"ca",
                "date_posted":"all",       #prams: today, 3days, week, month,all
                #"work_from_home":"true"
        }
        # Make the API request:
        print(f"Making request to {API_URL} with headers {headers} and params {params}")
        response = requests.get(API_URL, headers=headers,params=params)
        data = response.json()

        with open('job_output.json', 'w') as file1:
            json.dump(data, file1, indent=4)  # Pretty-print
        print("✅ Job information have been written to job_output.json")

        results = [
            {
            "job_id": job.get("job_id"),  # 👈 always include job_id!
            "search_id": job.get("job_id"),  # optional, for clarity in frontend if you want
            "job_title": job.get("job_title"),
            "employer_name": job.get("employer_name"),
            "job_location": job.get("job_location"),
            "job_posted_at_datetime_utc": job.get("job_posted_at_datetime_utc"),
            "job_google_link": job.get("job_google_link"),
            "employer_logo": job.get("employer_logo"),
            "employer_website": job.get("employer_website"),
            "job_is_remote": job.get("job_is_remote"),
            "job_employment_type": job.get("job_employment_type"),
            "job_salary": job.get("job_salary") or extract_salary(job.get("job_description")),
            "job_description": job.get("job_description") or extract_salary(job.get("job_description") or ""),
            }
            for job in data.get("data", [])            
        ]
        return {"status": "OK", "results": results}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
