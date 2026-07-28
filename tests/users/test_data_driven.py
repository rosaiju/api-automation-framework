import pytest
import allure
from utils.data_loader import json_to_pytest_params, load_json
from utils.assertions import assert_status, assert_response_time, assert_field_present


CREATE_PARAMS = json_to_pytest_params("users.json", ["firstName", "lastName", "age"])
SEARCH_PARAMS = json_to_pytest_params("search_queries.json", ["query", "min_results"])


@allure.feature("Users")
@allure.story("Data-Driven Tests")
class TestDataDriven:

    @allure.title("Create user from dataset - {first_name} {last_name}")
    @pytest.mark.parametrize("first_name,last_name,age", CREATE_PARAMS)
    @pytest.mark.regression
    def test_create_user_from_dataset(self, user_client, first_name, last_name, age):
        response = user_client.create_user(
            first_name=first_name, last_name=last_name, age=int(age)
        )

        assert_status(response, 201)
        assert_response_time(response)
        body = response.json()
        assert body["firstName"] == first_name
        assert body["lastName"] == last_name

    @allure.title("Search users from dataset - query '{query}'")
    @pytest.mark.parametrize("query,min_results", SEARCH_PARAMS)
    @pytest.mark.regression
    def test_search_users_from_dataset(self, user_client, query, min_results):
        response = user_client.search_users(query)

        assert_status(response, 200)
        assert_response_time(response)
        body = response.json()
        assert_field_present(body, "users", "total")
        assert body["total"] >= int(min_results)

    @allure.title("Bulk create users - all 5 dataset users succeed")
    @pytest.mark.regression
    def test_bulk_create_from_json(self, user_client):
        users = load_json("users.json")
        results = []

        for user in users:
            response = user_client.create_user(
                first_name=user["firstName"],
                last_name=user["lastName"],
                age=user["age"],
            )
            assert_status(response, 201)
            results.append(response.json())

        assert len(results) == len(users)
        for result in results:
            assert "id" in result
