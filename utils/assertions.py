import requests


def assert_status(response: requests.Response, expected: int):
    assert response.status_code == expected, (
        f"Expected {expected}, got {response.status_code}. Body: {response.text[:500]}"
    )


def assert_response_time(response: requests.Response, max_seconds: float = 2.0):
    elapsed = response.elapsed.total_seconds()
    assert elapsed < max_seconds, (
        f"Response too slow: {elapsed:.2f}s (limit: {max_seconds}s)"
    )


def assert_field_present(body: dict, *fields: str):
    for field in fields:
        assert field in body, f"Missing required field: '{field}' in response body"


def assert_no_extra_fields(body: dict, known_fields: set):
    unexpected = set(body.keys()) - known_fields
    assert not unexpected, f"Schema drift — unexpected fields: {unexpected}"


def assert_list_not_empty(body: dict, key: str):
    assert key in body, f"Key '{key}' not in response"
    assert len(body[key]) > 0, f"Expected non-empty list for '{key}'"
