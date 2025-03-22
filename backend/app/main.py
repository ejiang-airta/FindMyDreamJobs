from fastapi import FastAPI
from app.routes import user, job, resume, application, match, auth


app = FastAPI()

# Register API routes
app.include_router(user.router)
app.include_router(job.router)
app.include_router(resume.router)
app.include_router(application.router)
app.include_router(match.router)
app.include_router(auth.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to FindMyDreamJobs API"}