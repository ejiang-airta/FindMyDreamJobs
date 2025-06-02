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
#host = os.getenv("POSTGRES_HOST", "localhost")
# Default value for DATABASE_URL
DATABASE_URL = os.getenv("DATABASE_URL", f"postgresql+psycopg2://{username}:{password}@localhost/job_db")

# debugging print the DATABASE_URL:
print(f"DATABASE_URL: {DATABASE_URL}")