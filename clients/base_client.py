import requests
from config.settings import TIMEOUT


class BaseClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})

    def get(self, endpoint: str, params: dict = None) -> requests.Response:
        return self.session.get(
            f"{self.base_url}{endpoint}", params=params, timeout=TIMEOUT
        )

    def post(self, endpoint: str, payload: dict = None) -> requests.Response:
        return self.session.post(
            f"{self.base_url}{endpoint}", json=payload, timeout=TIMEOUT
        )

    def put(self, endpoint: str, payload: dict = None) -> requests.Response:
        return self.session.put(
            f"{self.base_url}{endpoint}", json=payload, timeout=TIMEOUT
        )

    def patch(self, endpoint: str, payload: dict = None) -> requests.Response:
        return self.session.patch(
            f"{self.base_url}{endpoint}", json=payload, timeout=TIMEOUT
        )

    def delete(self, endpoint: str) -> requests.Response:
        return self.session.delete(f"{self.base_url}{endpoint}", timeout=TIMEOUT)

    def set_auth_token(self, token: str):
        self.session.headers.update({"Authorization": f"Bearer {token}"})
