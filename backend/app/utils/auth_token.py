# File: /backend/app/utils/token.py
# This module provides functions to generate and verify password reset tokens.

from itsdangerous import URLSafeTimedSerializer
from os import getenv

SECRET = getenv("SECRET_KEY", "super-secret-key")  # replace with secure secret!
serializer = URLSafeTimedSerializer(SECRET)

def generate_password_reset_token(user_id: int) -> str:
    return serializer.dumps({ "user_id": user_id }, salt="password-reset")

def verify_password_reset_token(token: str, max_age_seconds: int = 3600):
    try:
        data = serializer.loads(token, salt="password-reset", max_age=max_age_seconds)
        return data["user_id"]
    except Exception:
        return None
