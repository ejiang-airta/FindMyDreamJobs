# File: backend/app/routes/job_search.py

from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
import requests
import os

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
                "num_pages":"9",
                "country":"ca",
                "date_posted":"week",       #prams: today, 3days, week, month,all
                #"work_from_home":"true"
        }
        # Make the API request:
        response = requests.get(API_URL, headers=headers,params=params)
        data = response.json()

        results = [
            {
                "job_title": job.get("job_title"),
                "employer_name": job.get("employer_name"),
                "job_location": job.get("job_city"),
                "description": job.get("job_description"),
                "posted_at": job.get("job_posted_at_datetime_utc"),
                "redirect_url": job.get("job_google_link")
            }
            for job in data.get("data", [])
            
        ]
        return {"status": "OK", "results": results}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
