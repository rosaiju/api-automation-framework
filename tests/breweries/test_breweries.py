import pytest
import allure
from dacite import from_dict, Config
from models.brewery import Brewery

STRICT = Config(strict=False)  # Brewery API may add optional fields; we validate known ones
VALID_BREWERY_TYPES = {"micro", "nano", "regional", "brewpub", "large", "planning", "bar", "contract", "proprietor", "taproom", "closed"}


@allure.feature("Breweries")
class TestBreweries:

    @allure.story("GET /breweries")
    @allure.title("List breweries - returns list with valid schema")
    @pytest.mark.smoke
    def test_list_breweries_schema(self, brewery_client):
        response = brewery_client.list_breweries(per_page=5)

        assert response.status_code == 200
        breweries = response.json()
        assert len(breweries) > 0

        for item in breweries:
            b = from_dict(Brewery, item, config=STRICT)
            assert b.id is not None
            assert b.name is not None
            assert b.country is not None

    @allure.story("GET /breweries")
    @allure.title("List breweries - brewery_type is always a known value")
    @pytest.mark.schema
    def test_brewery_type_enum_validation(self, brewery_client):
        response = brewery_client.list_breweries(per_page=20)
        breweries = response.json()

        for item in breweries:
            assert item["brewery_type"] in VALID_BREWERY_TYPES, (
                f"Unknown brewery_type: {item['brewery_type']}"
            )

    @allure.story("GET /breweries/search")
    @allure.title("Search breweries - query '{query}' returns relevant results")
    @pytest.mark.parametrize("query", ["dog", "stone", "blue moon"])
    @pytest.mark.regression
    def test_search_breweries(self, brewery_client, query):
        response = brewery_client.search_breweries(query)

        assert response.status_code == 200
        results = response.json()
        assert isinstance(results, list)
        for item in results:
            from_dict(Brewery, item, config=STRICT)  # Schema must hold for every result

    @allure.story("GET /breweries")
    @allure.title("Filter by type - {brewery_type} results all match requested type")
    @pytest.mark.parametrize("brewery_type", ["micro", "brewpub", "large"])
    @pytest.mark.regression
    def test_filter_by_type(self, brewery_client, brewery_type):
        response = brewery_client.list_by_type(brewery_type)

        assert response.status_code == 200
        breweries = response.json()
        for item in breweries:
            assert item["brewery_type"] == brewery_type

    @allure.story("GET /breweries")
    @allure.title("Filter by city - San Diego results are in correct city")
    @pytest.mark.regression
    def test_filter_by_city(self, brewery_client):
        response = brewery_client.list_by_city("San Diego")

        assert response.status_code == 200
        breweries = response.json()
        for item in breweries:
            assert "San Diego" in (item.get("city") or ""), (
                f"Expected San Diego but got city: {item.get('city')}"
            )

    @allure.story("GET /breweries")
    @allure.title("Response time under 2 seconds")
    @pytest.mark.smoke
    def test_list_breweries_response_time(self, brewery_client):
        response = brewery_client.list_breweries()
        assert response.elapsed.total_seconds() < 2.0

    @allure.story("GET /breweries")
    @allure.title("Schema drift detection - no unexpected top-level fields")
    @pytest.mark.schema
    def test_no_schema_drift(self, brewery_client):
        known_fields = {
            "id", "name", "brewery_type", "address_1", "address_2", "address_3",
            "city", "state_province", "postal_code", "country", "longitude",
            "latitude", "phone", "website_url", "state", "street"
        }
        response = brewery_client.list_breweries(per_page=5)
        for item in response.json():
            unexpected = set(item.keys()) - known_fields
            assert not unexpected, f"Schema drift detected — new fields: {unexpected}"
