from clients.base_client import BaseClient
from config.settings import BASE_URL


class UserClient(BaseClient):
    def __init__(self):
        super().__init__(BASE_URL)

    def get_users(self, limit: int = 10, skip: int = 0):
        return self.get("/users", params={"limit": limit, "skip": skip})

    def get_user(self, user_id: int):
        return self.get(f"/users/{user_id}")

    def search_users(self, query: str):
        return self.get("/users/search", params={"q": query})

    def create_user(self, first_name: str, last_name: str, age: int):
        return self.post("/users/add", payload={
            "firstName": first_name,
            "lastName": last_name,
            "age": age,
        })

    def update_user(self, user_id: int, **kwargs):
        return self.put(f"/users/{user_id}", payload=kwargs)

    def patch_user(self, user_id: int, **kwargs):
        return self.patch(f"/users/{user_id}", payload=kwargs)

    def delete_user(self, user_id: int):
        return self.delete(f"/users/{user_id}")

    def get_user_posts(self, user_id: int):
        return self.get(f"/users/{user_id}/posts")
