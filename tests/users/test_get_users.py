import pytest
import allure
from dacite import from_dict
from models.user import UserListResponse


@allure.feature("Users")
@allure.story("GET /users")
class TestGetUsers:

    @allure.title("List users - returns valid schema with pagination metadata")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_list_users_schema(self, user_client):
        response = user_client.get_users(limit=10, skip=0)

        assert response.status_code == 200
        body = from_dict(UserListResponse, response.json())
        assert body.total > 0
        assert len(body.users) == 10

    @allure.title("List users - skip parameter returns different page of results")
    @pytest.mark.regression
    def test_list_users_pagination(self, user_client):
        page1 = user_client.get_users(limit=5, skip=0).json()
        page2 = user_client.get_users(limit=5, skip=5).json()

        ids_page1 = {u["id"] for u in page1["users"]}
        ids_page2 = {u["id"] for u in page2["users"]}
        assert ids_page1.isdisjoint(ids_page2), "Paginated pages should not share user IDs"

    @allure.title("List users - response time under 2 seconds")
    @pytest.mark.smoke
    def test_list_users_response_time(self, user_client):
        response = user_client.get_users()
        assert response.elapsed.total_seconds() < 2.0

    @allure.title("Get single user {user_id} - returns correct id in response")
    @pytest.mark.parametrize("user_id", [1, 2, 5])
    @pytest.mark.regression
    def test_get_single_user(self, user_client, user_id):
        response = user_client.get_user(user_id)

        assert response.status_code == 200
        body = response.json()
        assert body["id"] == user_id
        assert "firstName" in body
        assert "email" in body

    @allure.title("Get user - 404 for non-existent user")
    @pytest.mark.negative
    @pytest.mark.parametrize("user_id", [9999, 10000])
    def test_get_nonexistent_user_returns_404(self, user_client, user_id):
        response = user_client.get_user(user_id)
        assert response.status_code == 404

    @allure.title("Search users - query returns matching results")
    @pytest.mark.regression
    @pytest.mark.parametrize("query", ["John", "Emily", "James"])
    def test_search_users(self, user_client, query):
        response = user_client.search_users(query)

        assert response.status_code == 200
        body = response.json()
        assert "users" in body
        assert isinstance(body["users"], list)

    @allure.title("List users - all required fields present on every user")
    @pytest.mark.schema
    def test_list_users_required_fields(self, user_client):
        response = user_client.get_users(limit=5)
        users = response.json()["users"]

        required_fields = {"id", "firstName", "lastName", "email", "username", "age", "gender"}
        for user in users:
            missing = required_fields - set(user.keys())
            assert not missing, f"User {user.get('id')} is missing fields: {missing}"

    @allure.title("Get user's posts - returns list of posts for user")
    @pytest.mark.regression
    def test_get_user_posts(self, user_client):
        response = user_client.get_user_posts(user_id=1)

        assert response.status_code == 200
        body = response.json()
        assert "posts" in body
        for post in body["posts"]:
            assert post["userId"] == 1
