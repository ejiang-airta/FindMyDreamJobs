"""API tests for authentication endpoints."""

import pytest
from unittest.mock import patch


class TestSignup:
    def test_signup_success(self, client):
        resp = client.post("/auth/signup", json={
            "email": "newuser@example.com",
            "full_name": "New User",
            "password": "securepass123",
        })
        assert resp.status_code == 200
        data = resp.json()
        assert "user_id" in data
        assert data["user_id"] > 0

    def test_signup_duplicate_email(self, client, test_user):
        resp = client.post("/auth/signup", json={
            "email": test_user.email,
            "full_name": "Duplicate User",
            "password": "password123",
        })
        assert resp.status_code == 400
        assert "already exists" in resp.json()["detail"].lower()


class TestLogin:
    def test_login_success(self, client, test_user):
        resp = client.post("/auth/login", json={
            "email": "testuser@example.com",
            "password": "testpassword123",
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data["user_id"] == test_user.id
        assert data["email"] == test_user.email

    def test_login_wrong_password(self, client, test_user):
        resp = client.post("/auth/login", json={
            "email": "testuser@example.com",
            "password": "wrongpassword",
        })
        assert resp.status_code == 401

    def test_login_nonexistent_user(self, client):
        resp = client.post("/auth/login", json={
            "email": "nobody@example.com",
            "password": "password123",
        })
        assert resp.status_code == 401


class TestWhoami:
    def test_existing_user(self, client, test_user):
        resp = client.post("/auth/whoami", json={"email": test_user.email})
        assert resp.status_code == 200
        assert resp.json()["user_id"] == test_user.id

    def test_nonexistent_user(self, client):
        resp = client.post("/auth/whoami", json={"email": "unknown@example.com"})
        assert resp.status_code == 404

    def test_missing_email(self, client):
        resp = client.post("/auth/whoami", json={})
        assert resp.status_code == 400


class TestPasswordReset:
    def test_request_reset_nonexistent_email(self, client):
        resp = client.post("/auth/request-password-reset", json={
            "email": "nobody@example.com",
        })
        assert resp.status_code == 404

    @patch("app.routes.auth.send_password_reset_email")
    def test_request_reset_success(self, mock_send, client, test_user):
        resp = client.post("/auth/request-password-reset", json={
            "email": test_user.email,
        })
        assert resp.status_code == 200
        mock_send.assert_called_once()
