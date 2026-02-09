# File: backend/app/schemas/user_profile.py
# Pydantic schemas for JDI user profile/preferences
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class UserProfileBase(BaseModel):
    target_titles: Optional[list[str]] = None
    target_locations: Optional[list[str]] = None
    jdi_min_score: int = Field(default=60, ge=0, le=100)
    jdi_sources_enabled: Optional[list[str]] = None
    jdi_base_resume_ids: Optional[list[int]] = Field(default=None, max_length=3)
    jdi_resume_select_mode: str = Field(default="auto_best", pattern="^(auto_best|keyword_rules)$")
    jdi_resume_keyword_rules: Optional[dict] = None
    jdi_scan_window_days: int = Field(default=7, ge=1, le=7)
    jdi_custom_source_patterns: Optional[list[str]] = None


class UserProfileCreate(UserProfileBase):
    user_id: int


class UserProfileUpdate(UserProfileBase):
    """All fields optional for partial updates."""
    target_titles: Optional[list[str]] = None
    target_locations: Optional[list[str]] = None
    jdi_min_score: Optional[int] = Field(default=None, ge=0, le=100)
    jdi_sources_enabled: Optional[list[str]] = None
    jdi_base_resume_ids: Optional[list[int]] = Field(default=None, max_length=3)
    jdi_resume_select_mode: Optional[str] = Field(default=None, pattern="^(auto_best|keyword_rules)$")
    jdi_resume_keyword_rules: Optional[dict] = None
    jdi_scan_window_days: Optional[int] = Field(default=None, ge=1, le=7)
    jdi_custom_source_patterns: Optional[list[str]] = None


class UserProfileOut(UserProfileBase):
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
