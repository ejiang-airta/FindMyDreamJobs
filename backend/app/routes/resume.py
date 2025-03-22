from fastapi import APIRouter, UploadFile, File, Depends, Form
from sqlalchemy.orm import Session
from app.database.connection import SessionLocal
from app.models.resume import Resume
from datetime import datetime
import os
import uuid
from app.config.settings import UPLOAD_DIR

router = APIRouter()

UPLOAD_DIR = "uploads/resumes"

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 🔹 1. Upload Resume
@router.post("/upload-resume", tags=["Resumes"])
async def upload_resume(
    user_id: int = Form(...),  # 👈 FIXED HERE
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    filename = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    os.makedirs(UPLOAD_DIR, exist_ok=True)
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Placeholder parsed text (real extraction coming in Step 3)
    parsed_text = f"Uploaded resume: {file.filename}"

    new_resume = Resume(
        user_id=user_id,
        file_path=file_path,
        parsed_text=parsed_text,
        created_at=datetime.now()
    )
    db.add(new_resume)
    db.commit()
    db.refresh(new_resume)

    return {
        "message": "✅ Resume uploaded successfully",
        "resume_id": new_resume.id,
        "file_path": file_path
    }

# 🔹 2. Get All Resumes
@router.get("/resumes", tags=["Resumes"])
def get_resumes(db: Session = Depends(get_db)):
    resumes = db.query(Resume).all()
    return [
        {
            "id": resume.id,
            "user_id": resume.user_id,
            "file_path": resume.file_path,
            "parsed_text": resume.parsed_text,
            "created_at": resume.created_at,
        }
        for resume in resumes
    ]
