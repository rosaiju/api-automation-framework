import pytest
import allure
from dacite import from_dict
from models.auth import LoginSuccessResponse, AuthUser


@allure.feature("Authentication")
class TestAuth:

    @allure.story("POST /auth/login")
    @allure.title("Login - valid credentials return access and refresh tokens")
    @pytest.mark.smoke
    def test_login_success(self, auth_client):
        response = auth_client.login(username="emilys", password="emilyspass")

        assert response.status_code == 200
        body = from_dict(LoginSuccessResponse, response.json())
        assert len(body.accessToken) > 0
        assert len(body.refreshToken) > 0

    @allure.story("POST /auth/login")
    @allure.title("Login - invalid credentials return 400")
    @pytest.mark.negative
    def test_login_invalid_credentials(self, auth_client):
        response = auth_client.login(username="invaliduser", password="wrongpassword")
        assert response.status_code == 400

    @allure.story("GET /auth/me")
    @allure.title("Get current user - valid token returns authenticated user profile")
    @pytest.mark.smoke
    def test_get_current_user_with_token(self, auth_client, auth_token):
        response = auth_client.get_current_user(token=auth_token)

        assert response.status_code == 200
        body = response.json()
        assert "id" in body
        assert "username" in body
        assert "email" in body

    @allure.story("GET /auth/me")
    @allure.title("Get current user - request without token returns 401")
    @pytest.mark.negative
    def test_get_current_user_without_token(self, auth_client):
        from clients.auth_client import AuthClient
        fresh_client = AuthClient()  # No token set
        response = fresh_client.get("/auth/me")
        assert response.status_code == 401

    @allure.story("POST /auth/refresh")
    @allure.title("Refresh token - valid refresh token returns new access token")
    @pytest.mark.regression
    def test_refresh_token(self, auth_client, refresh_token_value):
        response = auth_client.refresh_token(refresh_token=refresh_token_value)

        assert response.status_code == 200
        body = response.json()
        assert "accessToken" in body
        assert len(body["accessToken"]) > 0

    @allure.story("POST /auth/login")
    @allure.title("Login - token is session-scoped and reusable")
    @pytest.mark.regression
    def test_session_scoped_token_reuse(self, auth_token):
        # Token from session fixture used in multiple tests — validates fixture pattern
        assert auth_token is not None
        assert len(auth_token) > 0
