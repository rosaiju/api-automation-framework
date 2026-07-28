import pytest
import allure
from clients.product_client import ProductClient
from utils.assertions import assert_status, assert_response_time, assert_field_present, assert_list_not_empty


@pytest.fixture(scope="module")
def product_client():
    return ProductClient()


@allure.feature("Products")
class TestProducts:

    @allure.title("List products - returns paginated list with schema")
    @pytest.mark.smoke
    def test_list_products_schema(self, product_client):
        response = product_client.list_products(limit=10)

        assert_status(response, 200)
        assert_response_time(response)
        body = response.json()
        assert_field_present(body, "products", "total", "skip", "limit")
        assert_list_not_empty(body, "products")

        for p in body["products"]:
            assert_field_present(p, "id", "title", "price", "stock", "rating", "category")

    @allure.title("Get single product - id {product_id} returns correct data")
    @pytest.mark.parametrize("product_id", [1, 5, 10])
    @pytest.mark.regression
    def test_get_single_product(self, product_client, product_id):
        response = product_client.get_product(product_id)

        assert_status(response, 200)
        body = response.json()
        assert body["id"] == product_id
        assert body["price"] > 0
        assert 0 <= body["rating"] <= 5

    @allure.title("Search products - query '{query}' returns relevant results")
    @pytest.mark.parametrize("query", ["phone", "laptop", "shirt"])
    @pytest.mark.regression
    def test_search_products(self, product_client, query):
        response = product_client.search_products(query)

        assert_status(response, 200)
        body = response.json()
        assert isinstance(body["products"], list)

    @allure.title("Get categories - returns non-empty list of strings")
    @pytest.mark.smoke
    def test_get_categories(self, product_client):
        response = product_client.get_categories()

        assert_status(response, 200)
        categories = response.json()
        assert isinstance(categories, list)
        assert len(categories) > 0

    @allure.title("Filter by category - all results match requested category")
    @pytest.mark.regression
    def test_filter_by_category(self, product_client):
        # First get a valid category dynamically
        categories_response = product_client.get_categories()
        categories = categories_response.json()
        category_slug = categories[0]["slug"]

        response = product_client.get_by_category(category_slug)
        assert_status(response, 200)
        body = response.json()
        for product in body["products"]:
            assert product["category"].lower() == categories[0]["name"].lower()

    @allure.title("Add product - returns 201 with new product data")
    @pytest.mark.smoke
    def test_add_product(self, product_client):
        response = product_client.add_product(
            title="Test Automation Widget", price=49.99, stock=100
        )
        assert_status(response, 201)
        body = response.json()
        assert body["title"] == "Test Automation Widget"
        assert body["price"] == 49.99
        assert "id" in body

    @allure.title("Products have valid price range (> 0 and < 10000)")
    @pytest.mark.schema
    def test_product_price_range(self, product_client):
        response = product_client.list_products(limit=20)
        for product in response.json()["products"]:
            assert 0 < product["price"] < 10000, (
                f"Product {product['id']} has suspicious price: {product['price']}"
            )

    @allure.title("Product rating is always between 0 and 5")
    @pytest.mark.schema
    def test_product_rating_bounds(self, product_client):
        response = product_client.list_products(limit=20)
        for product in response.json()["products"]:
            assert 0 <= product["rating"] <= 5, (
                f"Product {product['id']} has invalid rating: {product['rating']}"
            )

    @allure.title("Get non-existent product returns 404")
    @pytest.mark.negative
    def test_get_missing_product(self, product_client):
        response = product_client.get_product(99999)
        assert_status(response, 404)
