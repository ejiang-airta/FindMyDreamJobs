# ✅ File: backend/app/routes/auth.py 
# User Authentication APIs

from fastapi import APIRouter, HTTPException, Request, Depends, Body
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.models.user import User

router = APIRouter()

@router.post("/auth/whoami", tags=["Auth"])
def whoami(payload: dict = Body(...), db: Session = Depends(get_db)):
    email = payload.get("email")
    name = payload.get("name")

    if not email:
        raise HTTPException(status_code=400, detail="Missing email.")

    user = db.query(User).filter(User.email == email).first()

    if not user:
        user = User(
            email=email,
            full_name=name or "",  # ✅ use full_name instead of name
            hashed_password="",     # ✅ dummy for now
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    return {"user_id": user.id}

@router.post("/signup")
def signup(email: str, password: str):
    return {"message": f"User {email} registered successfully"}

@router.post("/login")
def login(email: str, password: str):
    return {"message": f"User {email} logged in"}
