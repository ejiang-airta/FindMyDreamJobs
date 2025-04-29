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
        'query': 'director engineering in Vancouver Canada',
        'page': 1,
        'num_pages': 8,
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
    

# Fetch jobs
jobs = fetch_jobs()

# Sort jobs by post date descending
def parse_date(dt_str):
    try:
        return datetime.datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
    except Exception:
        return datetime.datetime.min

jobs = sorted(
    jobs,
    key=lambda j: parse_date(j.get('job_posted_at_datetime_utc', '') or ''),
    reverse=True
)

# Display sorted jobs
display_jobs(jobs)

# Save jobs to HTML file with clickable links
def save_jobs_to_html(jobs, filename='job_output.html'):
    """Generate an HTML file from job postings with clickable links."""
    html_lines = [
        '<!DOCTYPE html>',
        '<html lang="en">',
        '<head><meta charset="UTF-8"><title>Job Postings</title></head>',
        '<body>',
        '<h1>Job Postings</h1>'
    ]
    for idx, job in enumerate(jobs, start=1):
        title = job.get('job_title', 'N/A')
        company = job.get('employer_name', 'N/A')
        location = job.get('job_location', 'N/A')
        posted = job.get('job_posted_at_datetime_utc', 'N/A')
        salary = job.get('job_salary', 'N/A')
        min_salary = job.get('job_min_salary', 'N/A')
        max_salary = job.get('job_max_salary', 'N/A')
        description = job.get('job_description', '')
        link = job.get('job_google_link', '#')

        # Job title header
        html_lines.append(f'<h2>Job {idx}: {title}</h2>')
        # Bullet list of metadata
        html_lines.append('<ul>')
        for label, value in [
            ('Company', company),
            ('Location', location),
            ('Posted at', posted),
            ('Salary', salary),
            ('Min Salary', min_salary),
            ('Max Salary', max_salary)
        ]:
            html_lines.append(f'<li><strong>{label}:</strong> {value}</li>')
        html_lines.append('</ul>')
        # Description with paragraphs
        html_lines.append('<h3>Description:</h3>')
        for line in description.split('\n'):
            if line.strip():
                html_lines.append(f'<p>{line}</p>')
        # Apply link
        html_lines.append(f'<p><strong>Apply at:</strong> <a href="{link}" target="_blank">Click here to apply</a></p>')
        # Separator
        html_lines.append('<hr>')
    html_lines.extend(['</body>', '</html>'])
    with open(filename, 'w', encoding='utf-8') as f:
        f.write('\n'.join(html_lines))
    print(f"✅ Job information saved to {filename}")

save_jobs_to_html(jobs)
# Attempt to export to DOCX if python-docx is available
try:
    from docx import Document
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    from docx.opc.constants import RELATIONSHIP_TYPE
except ImportError:
    print("⚠️  python-docx not installed. Skipping DOCX export. Install with `pip install python-docx` to enable this feature.")
else:
    def add_hyperlink(paragraph, text, url):
        """Add a hyperlink to a python-docx paragraph."""
        part = paragraph.part
        r_id = part.relate_to(url, RELATIONSHIP_TYPE.HYPERLINK, is_external=True)
        hyperlink = OxmlElement('w:hyperlink')
        hyperlink.set(qn('r:id'), r_id)
        new_run = OxmlElement('w:r')
        rPr = OxmlElement('w:rPr')
        c = OxmlElement('w:color'); c.set(qn('w:val'), '0000FF')
        u = OxmlElement('w:u');    u.set(qn('w:val'), 'single')
        rPr.append(c); rPr.append(u)
        new_run.append(rPr)
        text_el = OxmlElement('w:t'); text_el.text = text
        new_run.append(text_el)
        hyperlink.append(new_run)
        paragraph._p.append(hyperlink)
        return hyperlink

    def save_jobs_to_docx(jobs, filename='job_output.docx'):
        """Generate a DOCX file from job postings with formatted headers and bullet points."""
        doc = Document()
        doc.add_heading('Job Postings', level=1)
        total = len(jobs)
        for idx, job in enumerate(jobs, start=1):
            title = job.get('job_title', 'N/A')
            company = job.get('employer_name', 'N/A')
            location = job.get('job_location', 'N/A')
            posted = job.get('job_posted_at_datetime_utc', 'N/A')
            salary = job.get('job_salary', 'N/A')
            min_salary = job.get('job_min_salary', 'N/A')
            max_salary = job.get('job_max_salary', 'N/A')
            description = job.get('job_description', '')
            link = job.get('job_google_link', '#')

            doc.add_heading(f'Job {idx}: {title}', level=2)
            for label, value in [
                ('Company', company),
                ('Location', location),
                ('Posted at', posted),
                ('Salary', salary),
                ('Min Salary', min_salary),
                ('Max Salary', max_salary)
            ]:
                p = doc.add_paragraph(style='List Bullet')
                p.add_run(f'{label}: {value}')

            if description:
                desc_para = doc.add_paragraph()
                desc_run = desc_para.add_run('Description:')
                desc_run.bold = True
                for line in description.split('\n'):
                    if line.strip():
                        doc.add_paragraph(line)

            link_para = doc.add_paragraph()
            link_para.add_run('Apply at: ')
            add_hyperlink(link_para, 'Click here to apply', link)

            if idx < total:
                doc.add_page_break()

        doc.save(filename)
        print(f"✅ Job information saved to {filename}")

    save_jobs_to_docx(jobs)
# def main():
#     schedule.every(1).day.at("11:36").do(fetch_jobs)  # Run daily at 8 AM
#     while True:
#         schedule.run_pending()
#         time.sleep(60)

# if __name__ == "__main__":
#     main()