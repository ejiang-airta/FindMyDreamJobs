# ✅ File: backend/app/routes/dashboard.py
# Handles:
# Anything related to post-login user content
# Fetching data/stats for the user’s dashboard
# Wizard state/progress (since it’s an onboarding/usage assistant) */

from fastapi import APIRouter, HTTPException, Request, Depends, Body
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.models.user import User

router = APIRouter()

@router.post("/wizard/progress", tags=["Wizard"])
def update_wizard_progress(payload: dict = Body(...), db: Session = Depends(get_db)):
    email = payload.get("email")
    progress = payload.get("step")

    if not email or not progress:
        raise HTTPException(status_code=400, detail="Missing email or step.")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    user.wizard_progress = progress
    db.commit()
    return {"message": "✅ Progress updated", "step": progress}

@router.post("/wizard/progress/get", tags=["Wizard"])
def get_wizard_progress(payload: dict = Body(...), db: Session = Depends(get_db)):
    email = payload.get("email")

    if not email:
        raise HTTPException(status_code=400, detail="Missing email.")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    return {"step": user.wizard_progress or "upload"}
