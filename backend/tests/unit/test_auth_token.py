"""Unit tests for app.utils.auth_token -- password reset token generation/verification."""

import pytest
from unittest.mock import patch
import time as _time
from app.utils.auth_token import generate_password_reset_token, verify_password_reset_token


class TestGenerateToken:
    def test_returns_nonempty_string(self):
        token = generate_password_reset_token(user_id=42)
        assert isinstance(token, str)
        assert len(token) > 10

    def test_different_users_different_tokens(self):
        t1 = generate_password_reset_token(user_id=1)
        t2 = generate_password_reset_token(user_id=2)
        assert t1 != t2


class TestVerifyToken:
    def test_roundtrip(self):
        token = generate_password_reset_token(user_id=99)
        user_id = verify_password_reset_token(token)
        assert user_id == 99

    def test_expired_token_returns_none(self):
        token = generate_password_reset_token(user_id=1)
        # Advance time by patching the time function used by itsdangerous
        real_time = _time.time
        with patch("itsdangerous.timed.time.time", side_effect=lambda: real_time() + 7200):
            result = verify_password_reset_token(token, max_age_seconds=3600)
        assert result is None

    def test_tampered_token_returns_none(self):
        token = generate_password_reset_token(user_id=1)
        tampered = token + "TAMPERED"
        result = verify_password_reset_token(tampered)
        assert result is None

    def test_random_string_returns_none(self):
        result = verify_password_reset_token("not-a-real-token-at-all")
        assert result is None

    def test_empty_string_returns_none(self):
        result = verify_password_reset_token("")
        assert result is None
