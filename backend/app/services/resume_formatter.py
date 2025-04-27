# ✅ File: backend/app/services/resume_formatter.py
# Description: Formats resume text into a Word document with specific styles and sections.
# This module is used to generate a formatted resume in .docx format.
#

from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from io import BytesIO
from datetime import datetime
import os
import re
from app.config.skills_config import SECTION_KEYWORDS

def clean_text(raw_text: str) -> str:
    # Collapse multiple blank lines, trim spaces
    cleaned = re.sub(r'\n{2,}', '\n', raw_text.strip())
    return cleaned

def parse_contact_block(lines):
    name = ""
    contact_lines = []
    linked_in = ""
    
    if lines:
        name = lines.pop(0).strip()
    
    while lines and ("@" in lines[0] or any(char.isdigit() for char in lines[0]) or "linkedin.com" in lines[0].lower()):
        contact_lines.append(lines.pop(0).strip())
    
    contact_info = " | ".join(contact_lines)
    return name, contact_info, lines

def is_section_title(line: str) -> bool:
    if not line.strip():
        return False
    words = line.strip().split()
    if len(words) > 5:
        return False
    return any(keyword.lower() in line.lower() for keyword in SECTION_KEYWORDS)

def is_company_location(line: str) -> bool:
    return bool(re.search(r',\s*\w+', line)) and not any(c in line for c in [":", "-", "/"])

def is_job_title_date(line: str) -> bool:
    return bool(re.search(r'\d{2}/\d{4}', line)) or ("present" in line.lower())

def generate_formatted_resume_docx(resume_text: str, is_user_approved: bool) -> BytesIO:
    doc = Document()
    output = BytesIO()
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Segoe UI'

    current_dir = os.path.dirname(os.path.abspath(__file__))
    image_dir = os.path.join(current_dir, "resource")
    image_path = os.path.join(image_dir, "horizontal_line.png")

    lines = clean_text(resume_text).split('\n')

    name, contact_info, lines = parse_contact_block(lines)

    # Header: Name
    p = doc.add_paragraph()
    run = p.add_run(name.upper())
    run.bold = True
    run.font.size = Pt(14)
    p.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

    # Header: Contact Info
    p = doc.add_paragraph()
    run = p.add_run(contact_info)
    run.font.size = Pt(10)
    p.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

    #doc.add_paragraph(" ")
    #doc.add_picture(image_path, width=None, height=None)

    IS_Summary = False
    inside_company_block = False

    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue

        if is_section_title(line):
            inside_company_block = False
            IS_Summary = 'SUMMARY' in line.upper()

            #doc.add_paragraph(" ")
            doc.add_picture(image_path, width=None, height=None)

            p = doc.add_paragraph()
            run = p.add_run(line.upper())
            run.bold = True
            run.font.size = Pt(12)
            continue

        if is_company_location(line):
            # split company and location, bold only the company
            p = doc.add_paragraph()
            if '|' in line:
                # pipe separator: Company | Location
                parts_pipe = line.split('|', 1)
                company = parts_pipe[0].strip()
                location = parts_pipe[1].strip()
                # bold company
                run = p.add_run(company)
                run.bold = True
                run.font.size = Pt(11)
                # non-bold separator + location
                run2 = p.add_run(' | ' + location)
                run2.bold = False
                run2.font.size = Pt(11)
            else:
                # comma separator: Company, Location
                parts = line.split(',', 1)
                company = parts[0].strip()
                location = parts[1].strip() if len(parts) > 1 else ''
                run = p.add_run(company)
                run.bold = True
                run.font.size = Pt(11)
                if location:
                    run2 = p.add_run(', ' + location)
                    run2.bold = False
                    run2.font.size = Pt(11)
            inside_company_block = True
            continue

        if inside_company_block and is_job_title_date(line):
            # split job title and dates, bold only the title
            p = doc.add_paragraph()
            if '|' in line:
                # pipe separator: Title | Dates
                parts_pipe = line.split('|', 1)
                title = parts_pipe[0].strip()
                dates = parts_pipe[1].strip()
                # bold title
                run = p.add_run(title)
                run.bold = True
                run.font.size = Pt(11)
                # non-bold separator + dates
                run2 = p.add_run(' | ' + dates)
                run2.bold = False
                run2.font.size = Pt(11)
            else:
                # find where the date portion begins
                m = re.search(r'\d{1,2}/\d{4}', line)
                idx = m.start() if m else line.lower().find('present')
                if idx is not None and idx >= 0:
                    # split into title and date, stripping trailing separators
                    title = line[:idx].rstrip(' -–—')
                    dates = line[idx:].strip()
                    # bold title
                    run = p.add_run(title)
                    run.bold = True
                    run.font.size = Pt(11)
                    # non-bold space + dates
                    run2 = p.add_run(' ' + dates)
                    run2.bold = False
                    run2.font.size = Pt(11)
                else:
                    # fallback: whole line normal
                    run = p.add_run(line)
                    run.bold = False
                    run.font.size = Pt(11)
            inside_company_block = False
            continue

        if line.startswith("-"):
            p = doc.add_paragraph(line[1:].strip(), style='List Bullet')
        else:
            p = doc.add_paragraph()
            run = p.add_run(line)
            if IS_Summary:
                run.font.size = Pt(11)
            else:
                run.font.size = Pt(10)

    # Footer
    if not is_user_approved:
        section = doc.sections[0]
        footer = section.footer
        p = footer.paragraphs[0]
        run = p.add_run("Generated by FindMyDreamJobs.com – Not yet user approved.")
        run.font.size = Pt(8)

    doc.save(output)
    output.seek(0)
    return output

# Reference
resume_formatter_reference = generate_formatted_resume_docx
