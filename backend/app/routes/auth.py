# ✅ File: backend/app/routes/auth.py 
# User Authentication APIs

from fastapi import APIRouter, HTTPException, Request, Depends, Body
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.models.user import User
from pydantic import BaseModel


router = APIRouter()

class SignupRequest(BaseModel):
    email: str
    full_name: str

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

@router.post("/auth/signup", response_model=None, tags=["Auth"])
def signup(payload: dict = Body(...), db: Session = Depends(get_db)):
    email = payload.get("email")
    full_name = payload.get("full_name")
    password = payload.get("password")

    # Validate the payload:
    if not email or not full_name or not password:
            raise HTTPException(status_code=400, detail="Missing fields.")

    # Check if the user already exists:
    existing = db.query(User).filter(User.email == email).first()

    if existing:
        raise HTTPException(status_code=400, detail="User already exists.")
    
    # Create the user:
    hashed_pw = password + "_fakehash"  # 🔒 Replace with real hashing later

    user = User(
        email=email,
        full_name=full_name,
        hashed_password=hashed_pw,  # ✅ placeholder for now
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {"message": f"✅ User {email} signed up!", "user_id": user.id}

@router.post("/login")
def login(email: str, password: str):
    return {"message": f"User {email} logged in"}
