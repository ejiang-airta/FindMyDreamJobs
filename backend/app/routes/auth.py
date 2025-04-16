# ✅ File: backend/app/routes/auth.py 
# User Authentication APIs

from fastapi import APIRouter, HTTPException, Depends, Body
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.models.user import User
from pydantic import BaseModel
from passlib.context import CryptContext  # ✅ Added for password hashing

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")  # ✅ Use bcrypt

class SignupRequest(BaseModel):
    email: str
    full_name: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

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
            full_name=name or "",
            hashed_password="",
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    return {"user_id": user.id}

@router.post("/auth/signup", tags=["Auth"])
def signup(payload: SignupRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="User already exists.")

    hashed_pw = pwd_context.hash(payload.password)
    user = User(
        email=payload.email,
        full_name=payload.full_name,
        hashed_password=hashed_pw,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": f"✅ User {payload.email} signed up!", "user_id": user.id}

@router.post("/auth/login", tags=["Auth"])
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not pwd_context.verify(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {
        "user_id": user.id,
        "email": user.email,
        "name": user.full_name,  # ✅ Add this line if it's not already included
        "message": "✅ Login successful!"
    }
