from clients.base_client import BaseClient
from config.settings import BASE_URL


class AuthClient(BaseClient):
    def __init__(self):
        super().__init__(BASE_URL)

    def login(self, username: str, password: str, expires_in_mins: int = 30):
        return self.post("/auth/login", payload={
            "username": username,
            "password": password,
            "expiresInMins": expires_in_mins,
        })

    def get_current_user(self, token: str):
        self.set_auth_token(token)
        return self.get("/auth/me")

    def refresh_token(self, refresh_token: str):
        return self.post("/auth/refresh", payload={
            "refreshToken": refresh_token,
            "expiresInMins": 30,
        })
