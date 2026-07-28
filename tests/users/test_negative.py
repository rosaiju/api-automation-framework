import pytest
import allure
from utils.assertions import assert_status


@allure.feature("Users")
@allure.story("Negative / Edge Cases")
class TestUsersNegative:

    @allure.title("Get user with string ID returns 400 or 404")
    @pytest.mark.negative
    def test_get_user_string_id(self, user_client):
        response = user_client.get("/users/abc")
        assert response.status_code in (400, 404)

    @allure.title("Search with empty query returns results or empty list")
    @pytest.mark.negative
    def test_search_empty_query(self, user_client):
        response = user_client.search_users(query="")
        assert_status(response, 200)
        body = response.json()
        assert "users" in body

    @allure.title("Search with special characters does not crash API")
    @pytest.mark.negative
    @pytest.mark.parametrize("query", ["<script>", "'; DROP TABLE", "!@#$%^"])
    def test_search_special_characters(self, user_client, query):
        response = user_client.search_users(query=query)
        # API should never 500 on bad input
        assert response.status_code != 500

    @allure.title("Get users with limit=0 - API ignores limit and returns all (documented behavior)")
    @pytest.mark.negative
    def test_get_users_limit_zero(self, user_client):
        # DummyJSON treats limit=0 as no limit — this documents the API's known behavior
        response = user_client.get_users(limit=0, skip=0)
        assert_status(response, 200)
        body = response.json()
        assert "users" in body
        assert body["total"] > 0

    @allure.title("Get users with very large skip returns empty list")
    @pytest.mark.negative
    def test_get_users_skip_beyond_total(self, user_client):
        response = user_client.get_users(limit=10, skip=99999)
        assert_status(response, 200)
        body = response.json()
        assert len(body["users"]) == 0

    @allure.title("Get non-existent user returns 404 with error message")
    @pytest.mark.negative
    @pytest.mark.parametrize("user_id", [9999, 10000, 99999])
    def test_get_missing_user_error_body(self, user_client, user_id):
        response = user_client.get_user(user_id)
        assert_status(response, 404)
        body = response.json()
        assert "message" in body
