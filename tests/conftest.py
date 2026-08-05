import pytest
from clients.user_client import UserClient
from clients.auth_client import AuthClient
from clients.brewery_client import BreweryClient
from config.settings import TEST_USERNAME, TEST_PASSWORD


@pytest.fixture(scope="session")
def user_client():
    return UserClient()


@pytest.fixture(scope="session")
def auth_client():
    return AuthClient()


@pytest.fixture(scope="session")
def brewery_client():
    return BreweryClient()


@pytest.fixture(scope="session")
def login_response(auth_client):
    response = auth_client.login(username=TEST_USERNAME, password=TEST_PASSWORD)
    assert response.status_code == 200, f"Login failed: {response.text}"
    return response.json()


@pytest.fixture(scope="session")
def auth_token(login_response):
    return login_response["accessToken"]


@pytest.fixture(scope="session")
def refresh_token_value(login_response):
    return login_response["refreshToken"]


@pytest.fixture(scope="session")
def authenticated_user_client(auth_token):
    client = UserClient()
    client.set_auth_token(auth_token)
    return client


BREWERY_TYPES = ["micro", "nano", "regional", "brewpub", "large", "planning"]
