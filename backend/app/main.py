from fastapi import FastAPI
from app.routes import user, job, resume, application, match, auth, ai_optimization, ats
from fastapi.middleware.cors import CORSMiddleware
import logging
import sys
import os
from datetime import datetime
from app.config.settings import PROJECT_ROOT

# Root logger configuration
logger_dir  = os.path.join(PROJECT_ROOT, "dev tracking", "logging")

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


# Optional: Create a reusable logger for your app
app_logger = logging.getLogger("app")

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    app_logger.info("✅ Registered Routes:")
    for route in app.routes:
        app_logger.info(f"{route.path} → {route.methods}")

# Register API routes
app.include_router(user.router)
app.include_router(job.router)
app.include_router(resume.router)
app.include_router(application.router)
app.include_router(match.router)
app.include_router(auth.router)
app.include_router(ai_optimization.router)  # ✅ AI Resume Optimization API
app.include_router(ats.router)              # ✅ New ATS API


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins during dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Welcome to FindMyDreamJobs API"}