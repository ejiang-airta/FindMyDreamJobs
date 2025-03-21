from fastapi import FastAPI
from app.routes import resume, job, auth, match, application

app = FastAPI()

# Register API routes
app.include_router(auth.router)
app.include_router(resume.router)
app.include_router(job.router)
app.include_router(match.router)
app.include_router(application.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to FindMyDreamJobs API"}