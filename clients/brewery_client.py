from clients.base_client import BaseClient
from config.settings import BREW_BASE_URL


class BreweryClient(BaseClient):
    def __init__(self):
        super().__init__(BREW_BASE_URL)

    def list_breweries(self, page: int = 1, per_page: int = 10):
        return self.get("/breweries", params={"page": page, "per_page": per_page})

    def get_brewery(self, brewery_id: str):
        return self.get(f"/breweries/{brewery_id}")

    def search_breweries(self, query: str):
        return self.get("/breweries/search", params={"query": query})

    def list_by_city(self, city: str):
        return self.get("/breweries", params={"by_city": city, "per_page": 5})

    def list_by_type(self, brewery_type: str):
        return self.get("/breweries", params={"by_type": brewery_type, "per_page": 10})
