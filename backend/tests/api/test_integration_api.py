# File: backend/tests/api/test_integration_api.py
# API integration tests for Gmail OAuth integration endpoints
import pytest
import json
import base64
from unittest.mock import patch, MagicMock
from datetime import datetime, timezone
from app.models.user_integration import UserIntegration
from app.services.jdi.gmail_oauth import encode_state


TEST_FRONTEND_URL = "https://findmydreamjobs-pr-99.onrender.com"


@pytest.fixture()
def gmail_integration(db_session, test_user):
    """Insert a Gmail integration record and return it."""
    integration = UserIntegration(
        user_id=test_user.id,
        provider="gmail",
        status="active",
        scopes=["https://www.googleapis.com/auth/gmail.readonly"],
        refresh_token_enc="encrypted-refresh-token",
        access_token_enc="encrypted-access-token",
    )
    db_session.add(integration)
    db_session.flush()
    return integration


class TestGmailStatus:
    """Tests for GET /api/integrations/gmail/status."""

    def test_status_not_found(self, client, test_user):
        """404 when no Gmail integration exists."""
        res = client.get(f"/api/integrations/gmail/status?user_id={test_user.id}")
        assert res.status_code == 404

    def test_status_active(self, client, test_user, gmail_integration):
        """Returns integration status when it exists."""
        res = client.get(f"/api/integrations/gmail/status?user_id={test_user.id}")
        assert res.status_code == 200
        data = res.json()
        assert data["provider"] == "gmail"
        assert data["status"] == "active"
        assert data["user_id"] == test_user.id
        # Should NOT expose tokens
        assert "refresh_token_enc" not in data
        assert "access_token_enc" not in data

    def test_status_revoked(self, client, test_user, gmail_integration, db_session):
        """Returns revoked status."""
        gmail_integration.status = "revoked"
        db_session.flush()

        res = client.get(f"/api/integrations/gmail/status?user_id={test_user.id}")
        assert res.status_code == 200
        assert res.json()["status"] == "revoked"


class TestGmailConnect:
    """Tests for GET /api/integrations/gmail/connect."""

    @patch("app.routes.integration.get_authorization_url")
    def test_connect_returns_auth_url(self, mock_get_url, client, test_user):
        """Returns authorization URL for OAuth flow."""
        mock_get_url.return_value = "https://accounts.google.com/o/oauth2/auth?client_id=test"

        res = client.get(
            f"/api/integrations/gmail/connect"
            f"?user_id={test_user.id}&frontend_url={TEST_FRONTEND_URL}"
        )
        assert res.status_code == 200
        data = res.json()
        assert "authorization_url" in data
        assert data["authorization_url"].startswith("https://accounts.google.com")
        # Verify frontend_url was forwarded to the service
        mock_get_url.assert_called_once_with(test_user.id, TEST_FRONTEND_URL)

    @patch("app.routes.integration.get_authorization_url")
    def test_connect_failure(self, mock_get_url, client, test_user):
        """500 when OAuth URL generation fails."""
        mock_get_url.side_effect = Exception("Missing client ID")

        res = client.get(
            f"/api/integrations/gmail/connect"
            f"?user_id={test_user.id}&frontend_url={TEST_FRONTEND_URL}"
        )
        assert res.status_code == 500

    def test_connect_missing_frontend_url(self, client, test_user):
        """422 when frontend_url is omitted (now a required param)."""
        res = client.get(f"/api/integrations/gmail/connect?user_id={test_user.id}")
        assert res.status_code == 422


class TestGmailCallback:
    """Tests for GET /api/integrations/gmail/callback."""

    @patch("app.routes.integration.handle_oauth_callback")
    def test_callback_success(self, mock_callback, client, test_user):
        """Successful OAuth callback stores tokens and redirects to the correct frontend."""
        mock_callback.return_value = MagicMock()
        state = encode_state(test_user.id, TEST_FRONTEND_URL)

        res = client.get(
            f"/api/integrations/gmail/callback?code=test-code&state={state}",
            follow_redirects=False,
        )
        # Should redirect (302) directly to /settings (not /jdi/setup) on the correct frontend
        assert res.status_code == 302
        location = res.headers["location"]
        assert "jdi_connected=true" in location
        assert "/settings" in location
        assert TEST_FRONTEND_URL in location

    def test_callback_invalid_state(self, client):
        """400 when state parameter cannot be decoded as a valid user ID."""
        res = client.get("/api/integrations/gmail/callback?code=test-code&state=!!!invalid!!!")
        assert res.status_code == 400

    @patch("app.routes.integration.handle_oauth_callback")
    def test_callback_value_error(self, mock_callback, client, test_user):
        """Redirects with error flag on ValueError (e.g., invalid auth code)."""
        mock_callback.side_effect = ValueError("Invalid authorization code")
        state = encode_state(test_user.id, TEST_FRONTEND_URL)

        res = client.get(
            f"/api/integrations/gmail/callback?code=bad-code&state={state}",
            follow_redirects=False,
        )
        # Should redirect (302) to frontend with error flag
        assert res.status_code == 302
        assert "jdi_error=true" in res.headers["location"]


class TestGmailRevoke:
    """Tests for POST /api/integrations/gmail/revoke."""

    @patch("app.routes.integration.revoke_integration")
    def test_revoke_success(self, mock_revoke, client, test_user):
        """Successful revocation."""
        mock_revoke.return_value = True

        res = client.post(f"/api/integrations/gmail/revoke?user_id={test_user.id}")
        assert res.status_code == 200
        assert res.json()["status"] == "revoked"

    @patch("app.routes.integration.revoke_integration")
    def test_revoke_not_found(self, mock_revoke, client, test_user):
        """404 when no integration to revoke."""
        mock_revoke.return_value = False

        res = client.post(f"/api/integrations/gmail/revoke?user_id={test_user.id}")
        assert res.status_code == 404
