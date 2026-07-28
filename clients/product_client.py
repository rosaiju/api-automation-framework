from clients.base_client import BaseClient
from config.settings import BASE_URL


class ProductClient(BaseClient):
    def __init__(self):
        super().__init__(BASE_URL)

    def list_products(self, limit: int = 10, skip: int = 0):
        return self.get("/products", params={"limit": limit, "skip": skip})

    def get_product(self, product_id: int):
        return self.get(f"/products/{product_id}")

    def search_products(self, query: str):
        return self.get("/products/search", params={"q": query})

    def get_categories(self):
        return self.get("/products/categories")

    def get_by_category(self, category: str):
        return self.get(f"/products/category/{category}")

    def add_product(self, title: str, price: float, stock: int):
        return self.post("/products/add", payload={
            "title": title,
            "price": price,
            "stock": stock,
        })
