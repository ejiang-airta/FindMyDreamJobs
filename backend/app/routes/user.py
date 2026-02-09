from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.connection import SessionLocal
from app.models.user import User

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/users", tags=["Users"])
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return [
        {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "created_at": user.created_at,
        }
        for user in users
    ]

@router.post("/delete-user", tags=["Auth"])
def delete_user(payload: dict, db: Session = Depends(get_db)):
    """Delete a user and all associated data (cascade delete)."""
    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(status_code=400, detail="user_id is required")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)  # Cascade deletes: resumes, jobs, applications, saved_jobs, user_profile, user_integration, jdi_candidates
    db.commit()
    return {"message": f"User {user_id} deleted successfully"}
