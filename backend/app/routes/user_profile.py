# File: backend/app/routes/user_profile.py
# API routes for JDI user profile/preferences
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import SessionLocal
from app.models.user_profile import UserProfile
from app.models.user import User
from app.schemas.user_profile import UserProfileCreate, UserProfileUpdate, UserProfileOut
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/profile", tags=["User Profile"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/{user_id}", response_model=UserProfileOut)
def get_profile(user_id: int, db: Session = Depends(get_db)):
    """Get JDI preferences for a user. Returns 404 if no profile exists."""
    profile = db.query(UserProfile).filter_by(user_id=user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile


@router.put("/{user_id}", response_model=UserProfileOut)
def update_profile(user_id: int, body: UserProfileUpdate, db: Session = Depends(get_db)):
    """
    Create or update JDI preferences for a user.
    Uses upsert semantics: creates if not exists, updates if exists.
    Only updates fields that are provided (non-None).
    """
    # Verify user exists
    user = db.query(User).filter_by(id=user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    profile = db.query(UserProfile).filter_by(user_id=user_id).first()

    if not profile:
        # Create new profile with defaults + provided fields
        profile_data = body.model_dump(exclude_none=True)
        profile = UserProfile(user_id=user_id, **profile_data)
        db.add(profile)
    else:
        # Update only provided fields
        update_data = body.model_dump(exclude_none=True)
        for field, value in update_data.items():
            setattr(profile, field, value)

    db.commit()
    db.refresh(profile)
    return profile
