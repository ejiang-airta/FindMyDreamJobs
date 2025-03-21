# User Authentication APIs

from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/signup")
def signup(email: str, password: str):
    return {"message": f"User {email} registered successfully"}

@router.post("/login")
def login(email: str, password: str):
    return {"message": f"User {email} logged in"}
