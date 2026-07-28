import pytest
import allure
from dacite import from_dict
from models.user import CreateUserResponse, UpdateUserResponse


@allure.feature("Users")
@allure.story("POST/PUT/PATCH/DELETE /users")
class TestUserMutations:

    @allure.title("Create user - returns 201 with correct schema")
    @pytest.mark.smoke
    @pytest.mark.parametrize("first_name,last_name,age", [
        ("John", "Doe", 28),
        ("Jane", "Smith", 32),
        ("Alex", "Johnson", 25),
    ])
    def test_create_user(self, user_client, first_name, last_name, age):
        response = user_client.create_user(first_name=first_name, last_name=last_name, age=age)

        assert response.status_code == 201
        body = response.json()
        assert body["firstName"] == first_name
        assert body["lastName"] == last_name
        assert "id" in body

    @allure.title("Update user - PUT returns 200 with updated firstName")
    @pytest.mark.regression
    def test_update_user_put(self, user_client):
        response = user_client.update_user(user_id=1, firstName="UpdatedName")

        assert response.status_code == 200
        body = response.json()
        assert body["firstName"] == "UpdatedName"
        assert body["id"] == 1

    @allure.title("Update user - PATCH returns 200 with only patched field")
    @pytest.mark.regression
    def test_update_user_patch(self, user_client):
        response = user_client.patch_user(user_id=1, lastName="PatchedLastName")

        assert response.status_code == 200
        body = response.json()
        assert body["lastName"] == "PatchedLastName"

    @allure.title("Delete user - returns 200 with isDeleted flag")
    @pytest.mark.smoke
    def test_delete_user(self, user_client):
        response = user_client.delete_user(user_id=1)

        assert response.status_code == 200
        body = response.json()
        assert body["isDeleted"] is True
        assert body["id"] == 1

    @allure.title("Create user - response time under 2 seconds")
    @pytest.mark.smoke
    def test_create_user_response_time(self, user_client):
        response = user_client.create_user(first_name="Speed", last_name="Test", age=20)
        assert response.elapsed.total_seconds() < 2.0
