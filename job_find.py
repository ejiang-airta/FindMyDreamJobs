import requests
from bs4 import BeautifulSoup
import schedule
import datetime
import json
import time
import os

# RapidAPI instance
rapid_api_host = 'jsearch.p.rapidapi.com'
rapid_api_key = os.getenv("RAPIDAPI_KEY")
API_URL = f"https://{rapid_api_host}/search?query=director%20quality%20engineering%20in%20Vancouver%20Canada&page=1&num_pages=1&country=ca&date_posted=all"

def fetch_jobs():
    job_postings = []
    
    # jsearch API
    headers = {
        'x-rapidapi-host': rapid_api_host.encode("ascii", "ignore").decode(),
        'x-rapidapi-key': rapid_api_key.encode("ascii", "ignore").decode()
        }
    # params = {'query': 
    #     'director%20quality%20engineering%20jobs%20in%20Vancouver&page=1&num_pages=9&country=CA'}

    params = {
        'query': 'director quality engineering in Vancouver Canada',
        'page': 1,
        'num_pages': 4,
        'job_country': 'ca',
        'date_posted': 'all'
    }
    response = requests.get(API_URL, headers=headers,params=params)

    data = response.json()
    #job_postings.extend(data['results'])
    job_postings = data.get("data")

    with open('job_output.json', 'w') as file1:
        json.dump(data, file1, indent=4)  # Pretty-print
        print("✅ Job information have been written to job_output.json")

    return job_postings

def display_jobs(jobs):
    # Display jobs in a user-friendly format
    print("*****Printing Job posting*****")
    iStart = 1

    for job in jobs:        
        print(f"***Fond job Number: {iStart}***")
        print(f"**Title: {job['job_title']}**")
        print(f"**Location: {job.get('job_location', 'N/A')}**")
        print(f"**Company: {job.get('employer_name', 'N/A')}**")
        print("-"*30)
        print(f"***Job Description: {job.get('job_description', 'N/A')}***")
        print("-"*30)
        print(f"**Posted at: {job.get('job_posted_at_datetime_utc', 'N/A')}**")
        print(f"**Salary: {job.get('job_salary', 'N/A')}**")
        print(f"**Min Salary: {job.get('job_min_salary', 'N/A')}**")
        print(f"**Max Salary: {job.get('job_max_salary', 'N/A')}**")
        print(f"**Apply at: <a href='{job.get('job_google_link', '#')}' target='_blank'>Click here to apply</a>**")
        print("-"*60)

        iStart += 1    
    

# Fetch and display jobs
jobs = fetch_jobs()

display_jobs(jobs)

# def main():
#     schedule.every(1).day.at("11:36").do(fetch_jobs)  # Run daily at 8 AM
#     while True:
#         schedule.run_pending()
#         time.sleep(60)

# if __name__ == "__main__":
#     main()