# File: /backend/app/config/settings.py
from dotenv import load_dotenv
import os

# Set Project Root: Job_App/
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))

# Set App directory: backend/app/
APP_DIR = os.path.join(PROJECT_ROOT, "backend", "app")

# Set actual folders
UPLOAD_DIR = os.path.join(APP_DIR, "uploads", "resumes")
TEMP_DIR = os.path.join(APP_DIR, "temp")

# debugging print the above folder pathR:
# print("📁 PROJECT_ROOT:", PROJECT_ROOT)
# print("📁 APP_DIR     :", APP_DIR)
# print("📁 UPLOAD_DIR  :", UPLOAD_DIR)
# print("📁 TEMP_DIR    :", TEMP_DIR)

# Load environment variables from a .env file, need "pip install python-dotenv" for it to work
load_dotenv()

# Database configuration:
username = os.getenv("POSTGRES_USER", "user")
password = os.getenv("POSTGRES_PASSWORD", "password")

# In preview environments use the isolated preview DB so CI tests never write to production.
# ENV is set to 'preview' for Render preview deployments via render.yaml previewValue.
# PREVIEW_DATABASE_URL lives in eugene-env-group (Render dashboard) — never in git.
# Alembic (migrations/env.py) imports DATABASE_URL from here, so it also targets the right DB.
_default_db = f"postgresql+psycopg2://{username}:{password}@localhost/job_db"
DATABASE_URL = (
    os.getenv("PREVIEW_DATABASE_URL")
    if os.getenv("ENV") == "preview" and os.getenv("PREVIEW_DATABASE_URL")
    else os.getenv("DATABASE_URL", _default_db)
)

# debugging print the DATABASE_URL:
print(f"ENV: {os.getenv('ENV')!r}")
print(f"PREVIEW_DATABASE_URL set: {bool(os.getenv('PREVIEW_DATABASE_URL'))}")
print(f"DATABASE_URL: {DATABASE_URL}")