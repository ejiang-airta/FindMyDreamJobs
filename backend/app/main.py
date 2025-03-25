from fastapi import FastAPI
from app.routes import user, job, resume, application, match, auth
from fastapi.middleware.cors import CORSMiddleware
import logging

logger = logging.getLogger("uvicorn")

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    logger.info("✅ Registered Routes:")
    for route in app.routes:
        logger.info(f"{route.path} → {route.methods}")

# Register API routes
app.include_router(user.router)
app.include_router(job.router)
app.include_router(resume.router)
app.include_router(application.router)
app.include_router(match.router)
app.include_router(auth.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # During dev, keep this open
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Welcome to FindMyDreamJobs API"}