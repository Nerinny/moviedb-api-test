import pytest
from helpers.request_helper import rate_movie, BEARER_TOKEN
from testdata.messages import TOO_HIGH_RATING_MESSAGE, TOO_LOW_RATING_MESSAGE, INVALID_PARAMS, UPDATED_SUCCESS, RESOURCE_NOT_FOUND, INVALID_ID
from testdata.response_schema import RATE_MOVIE_SCHEMA
import jsonschema

INVALID_TOKEN = '69e6abd3'
@pytest.mark.parametrize("token, expected_status", [
    (BEARER_TOKEN, 201),
    (INVALID_TOKEN, 401),
    (None, 401),
])
def test_add_rating_access_status_codes(token, expected_status):
    """Test API responses for 200 and 401 status codes."""
    response = rate_movie(token=token)
    assert response.status_code == expected_status, f"Expected {expected_status}, got {response.status_code}"

@pytest.mark.parametrize("rating, message", [
    (0, TOO_LOW_RATING_MESSAGE),
    ("aaa", TOO_LOW_RATING_MESSAGE),
    (100000, TOO_HIGH_RATING_MESSAGE),
])
def test_invalid_rating_response(rating, message):
    response = rate_movie(rating=rating)
    assert response.status_code == 400, f"Expected 400, got {response.status_code}"

    response_json = response.json()
    assert response_json["status_message"] == message

def test_wrong_parameters():
    response = rate_movie(rating=None)
    assert response.status_code == 400, f"Expected 400, got {response.status_code}"

    response_json = response.json()
    assert response_json["status_message"] == INVALID_PARAMS

def test_update_rating():
    response = rate_movie(rating=7.5)
    assert response.status_code == 201, f"Expected 201, got {response.status_code}"

    response_json = response.json()
    assert response_json["status_message"] == UPDATED_SUCCESS

def test_not_found_resource():
    response = rate_movie(movie_id=1234)
    assert response.status_code == 404, f"Expected 404, got {response.status_code}"

    response_json = response.json()
    assert response_json["status_message"] == RESOURCE_NOT_FOUND

@pytest.mark.parametrize("id", [0, -1, 'abc'])
def test_invalid_id(id):
    response = rate_movie(movie_id=0)
    assert response.status_code == 404, f"Expected 404, got {response.status_code}"

    response_json = response.json()
    assert response_json["status_message"] == INVALID_ID

def test_rate_movie_schema():
    """Test response schema"""
    response = rate_movie()
    try:
        jsonschema.validate(instance=response.json(), schema=RATE_MOVIE_SCHEMA)
    except jsonschema.exceptions.ValidationError as e:
        pytest.fail(f"Response body does not match schema: {e.message}")