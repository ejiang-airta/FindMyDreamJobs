# File: /backend/app/main.py
# Main entry point for the FastAPI application
from fastapi import FastAPI
from app.routes import user, job, resume, application, match, auth, ai_optimization, ats, dashboard, download, job_search, integration, jdi, user_profile
from fastapi.middleware.cors import CORSMiddleware
import logging
import sys
import os
from datetime import datetime
from app.config.settings import PROJECT_ROOT
from dotenv import load_dotenv
import httpx
import asyncio 

load_dotenv()

# Root logger configuration
logger_dir  = os.path.join(PROJECT_ROOT, "dev_tracking", "logging")
os.makedirs(logger_dir , exist_ok=True)

logging.basicConfig(
    level=logging.DEBUG,  # Use INFO if you don't want debug logs
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),  # ✅ Show logs in terminal
        logging.FileHandler(
            f"{logger_dir}/app_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log", mode='a'
        )  # ✅ Save logs to a timestamped file
    ]
)

origins = [
    "http://localhost:3000",      # ✅ Next.js dev server
    "http://127.0.0.1:3000",       # ✅ Alternate dev address
    "https://findmydreamjobs-frontend.onrender.com",  # ✅ Render frontend prod
    "https://.*\.onrender\.com",  # ✅ Allow all subdomains on Render
    "https://www.findmydreamjobs.com",  # ✅ optional: custom domain
    "https://findmydreamjobs.com",  # ✅ Render frontend staging
    "https://www.findmydreamjobs.com",  # ✅ Render frontend staging
]

# Optional: Create a reusable logger for your app
app_logger = logging.getLogger("app")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,    # Allow all origins during dev
    allow_credentials=True,
    allow_origin_regex=r"https://findmydreamjobs-pr-\d+\.onrender\.com",  # ← This handles all PR numbers
    allow_methods=["*"],      # or list specific methods like ["POST", "GET"]
    allow_headers=["*"],      # or explicitly allow ["Authorization", "Content-Type"]
)

@app.on_event("startup")
async def startup_event():
    app_logger.info("✅ Registered Routes:")
    for route in app.routes:
        app_logger.info(f"{route.path} → {route.methods}")

    # 🧪 Seed E2E test user in preview/dev environments
    env = os.getenv("ENV", "production")
    if env in ["preview", "development"]:
        from app.database.connection import SessionLocal
        from app.models.user import User
        from app.utils.auth_token import pwd_context

        db = SessionLocal()
        try:
            # Check if E2E test user exists (credentials from frontend/tests/ui/helpers.ts)
            test_user = db.query(User).filter(User.email == "testuser@abc.com").first()

            if not test_user:
                # Create test user with exact credentials from helpers.ts
                hashed_pw = pwd_context.hash("test123")
                user = User(
                    email="testuser@abc.com",
                    full_name="test user1",
                    hashed_password=hashed_pw
                )
                db.add(user)
                db.commit()
                app_logger.info("✅ E2E test user seeded: testuser@abc.com")
            else:
                app_logger.info("✅ E2E test user already exists: testuser@abc.com")
        except Exception as e:
            app_logger.error(f"❌ Failed to seed E2E test user: {e}")
            db.rollback()
        finally:
            db.close()

    # 🚀 Only ping in production
    if os.getenv("ENVIRONMENT") == "production":
        await asyncio.sleep(3)
        try:
            async with httpx.AsyncClient() as client:
                res = await client.get("https://findmydreamjobs.onrender.com")
                app_logger.info(f"🌐 Self-ping OK: {res.status_code}")
        except Exception as e:
            app_logger.warning(f"🚫 Failed self-ping: {e}")


# Register API routes
app.include_router(ai_optimization.router)  # ✅ AI Resume Optimization API
app.include_router(application.router)
app.include_router(ats.router)              # ✅ New ATS API
app.include_router(auth.router)             # adding a prefix , prefix="/auth", tags=["auth"]
app.include_router(dashboard.router)        # ✅ Dashboard API
app.include_router(job.router)
app.include_router(match.router)
app.include_router(resume.router)
app.include_router(download.router)
app.include_router(user.router)
app.include_router(job_search.router)       # ✅ Job Search API
app.include_router(integration.router)      # ✅ Gmail Integration API (JDI)
app.include_router(jdi.router)              # ✅ JDI Candidate Feed API
app.include_router(user_profile.router)     # ✅ JDI User Profile/Preferences API



@app.get("/")
def read_root():
    return {"message": "Welcome to FindMyDreamJobs API"}