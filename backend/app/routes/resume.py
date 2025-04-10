# ✅ File: backend/app/routes/resume.py
# Resume Management APIs:
import os
import uuid
import pdfplumber  # 👈 Install it using: pip install pdfplumber
from docx import Document  # DOCX Support
from fastapi import APIRouter, UploadFile, File, Depends, Form, HTTPException
from sqlalchemy.orm import Session
from app.database.connection import get_db, SessionLocal
from app.models.resume import Resume
from datetime import datetime, timezone
from app.config.settings import UPLOAD_DIR
from fastapi.responses import FileResponse
from app.services.file_utils import generate_resume_file, cleanup_file
from app.services.ats_scoring import calculate_ats_score  # 👈 Import ATS scoring function


router = APIRouter()

UPLOAD_DIR = "uploads/resumes"

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def extract_text_from_file(file_path: str) -> str:
    """Extract text from PDF, DOCX, or TXT files with proper error handling."""
    extension = os.path.splitext(file_path)[1].lower()

    try:
        if extension == ".pdf":
            text = ""
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() + "\n"
            return text.strip()
        elif extension == ".docx":
            doc = Document(file_path)
            return "\n".join([para.text for para in doc.paragraphs]).strip()

        elif extension == ".txt":
            # Try different encodings
            encodings = ["utf-8", "latin-1", "ISO-8859-1"]
            for encoding in encodings:
                try:
                    with open(file_path, "r", encoding=encoding) as f:
                        return f.read().strip()
                except UnicodeDecodeError:
                    continue  # Try next encoding

            # If all encodings fail, return an error
            return "❌ Error: Unsupported text file encoding."
        else:
            return f"❌ Error: Unsupported file format '{extension}'. Supported: PDF, DOCX, TXT."

    except Exception as e:
        return f"❌ Error processing file: {str(e)}"

# 🔹 1. Upload Resume
@router.post("/upload-resume", tags=["Resumes"])
async def upload_resume(
    user_id: int = Form(...),  # 👈 FIXED HERE
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    filename = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    #file_path = os.path.join("backend/app/uploads/resumes", filename)


    os.makedirs(UPLOAD_DIR, exist_ok=True)
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # 🔹 Extract text from PDF, DOCX, or TXT
    extracted_text = extract_text_from_file(file_path)

    # right after extraction, call the ATS scoring engine:
    formatting_score, _, _ = calculate_ats_score(extracted_text)
    ats_score_initial = formatting_score  # 👈 only store the numeric score


    # ✅ If extraction fails (unsupported format), raise an HTTPException (NO DB ENTRY)
    if extracted_text.startswith("❌ Error:"):
        os.remove(file_path)  # Clean up the invalid file
        raise HTTPException(status_code=400, detail=extracted_text)

    # ✅ If valid, store resume in DB
    new_resume = Resume(
        user_id=user_id,
        resume_name=file.filename,  # 👈 Store the original filename
        file_path=file_path,
        parsed_text=extracted_text,     # 👈 Store extracted tex# 👈 Now we save the actual text!
        ats_score_initial=ats_score_initial,
        created_at=datetime.now(timezone.utc)
    )
    db.add(new_resume)
    db.commit()
    db.refresh(new_resume)

    return {
        "message": "✅ Resume uploaded successfully",
        "resume_id": new_resume.id,
        "resume_name": new_resume.resume_name,
        "file_path": file_path
    }

# 🔹 2. Get All Resumes
@router.get("/resumes", tags=["Resumes"])
def get_all_resumes(db: Session = Depends(get_db)):
    resumes = db.query(Resume).all()
    return [
        {
            "id": r.id,
            "user_id": r.user_id,
            "file_path": r.file_path,
            "parsed_text": r.parsed_text,
            "optimized_text": r.optimized_text,
            "is_ai_generated": r.is_ai_generated,
            "is_user_approved": r.is_user_approved,
            "ats_score_initial": r.ats_score_initial or 0,
            "ats_score_final": r.ats_score_final or 0,
            "created_at": r.created_at.isoformat() if r.created_at else None,
            "updated_at": r.updated_at.isoformat() if r.updated_at else None,
        }
        for r in resumes
    ]
# @router.get("/download-resume/{resume_id}", tags=["Resumes"])
# def download_resume(resume_id: int, db: Session = Depends(get_db)):
#     resume = db.query(Resume).filter(Resume.id == resume_id).first()
#     if not resume or not resume.optimized_text:
#         raise HTTPException(status_code=404, detail="Optimized resume not found.")

#     buffer = io.BytesIO()
#     buffer.write(resume.optimized_text.encode("utf-8"))
#     buffer.seek(0)

#     filename = f"optimized_resume_{resume_id}.txt"
#     return StreamingResponse(buffer, media_type="text/plain", headers={
#         "Content-Disposition": f"attachment; filename={filename}"
#     })

# 🔹 3. Download Resume
@router.get("/download-resume/{resume_id}", tags=["Resume"])
def download_resume(resume_id: int, db: Session = Depends(get_db)):
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    # ✅ Pick optimized or original
    content = resume.optimized_text or resume.parsed_text or ""
    
    if not content:
        raise HTTPException(status_code=400, detail="No resume content available.")

    # ✅ Generate temp file
    filepath, filename = generate_resume_file(resume_id, content, is_optimized=bool(resume.optimized_text))

    # ✅ Return FileResponse and delete file after response is sent
    response = FileResponse(
        path=filepath,
        filename=filename,
        media_type="text/plain",
    )

    # ⚠️ WARNING: You cannot delete the file *before* returning the response
    # To safely clean it up, use a background task or let user know it's temporary

    # Option 1: Return the file and ask user to download quickly
    # Then delete after a small delay using BackgroundTasks
    from fastapi import BackgroundTasks

    def delete_file():
        cleanup_file(filepath)

    background_tasks = BackgroundTasks()
    background_tasks.add_task(delete_file)

    return FileResponse(
        path=filepath,
        filename=filename,
        media_type="text/plain",
        background=background_tasks
    )
# 🔹 4. Get Resume by resume ID
@router.get("/resumes/{resume_id}", tags=["Resumes"])
def get_resume_by_id(resume_id: int, db: Session = Depends(get_db)):
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")

    return {
        "id": resume.id,
        "user_id": resume.user_id,
        "file_path": resume.file_path,
        "parsed_text": resume.parsed_text,
        "optimized_text": resume.optimized_text,
        "is_ai_generated": resume.is_ai_generated,
        "is_user_approved": resume.is_user_approved,
        "ats_score_initial": resume.ats_score_initial or 0,
        "ats_score_final": resume.ats_score_final or 0,
        "created_at": resume.created_at.isoformat() if resume.created_at else None,
        "updated_at": resume.updated_at.isoformat() if resume.updated_at else None,
    }
# 🔹 5. Get all resumes for a specific user by user_id:
@router.get("/resumes/by-user/{user_id}", tags=["Resumes"])
def get_resumes_by_user(user_id: int, db: Session = Depends(get_db)):
    resumes = db.query(Resume).filter(Resume.user_id == user_id).all()

    if not resumes:
        raise HTTPException(status_code=404, detail="No resumes found for this user.")

    return [
        {
            "id": r.id,
            "user_id": r.user_id,
            "resume_name": r.resume_name,
            "file_path": r.file_path,
            "parsed_text": r.parsed_text,
            "optimized_text": r.optimized_text,
            "is_ai_generated": r.is_ai_generated,
            "is_user_approved": r.is_user_approved,
            "ats_score_initial": r.ats_score_initial or 0,
            "ats_score_final": r.ats_score_final or 0,
            "created_at": r.created_at.isoformat() if r.created_at else None,
            "updated_at": r.updated_at.isoformat() if r.updated_at else None,
        }
        for r in resumes
    ]
