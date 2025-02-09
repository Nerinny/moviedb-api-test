import pytest
from helpers.request_helper import get_top_rated_movies, rate_movie, BEARER_TOKEN
from langdetect import detect
from testdata.messages import INVALID_PAGE_MESSAGE
from testdata.response_schema import TOP_RATED_MOVIES_SCHEMA
import jsonschema

INVALID_TOKEN = '69e6abd3'
@pytest.mark.parametrize("token, expected_status", [
    (BEARER_TOKEN, 200),
    (INVALID_TOKEN, 401),
    (None, 401),
])
def test_access_status_codes(token, expected_status):
    """Test API responses for 200 and 401 status codes."""
    response = get_top_rated_movies(token=token)
    assert response.status_code == expected_status, f"Expected {expected_status}, got {response.status_code}"

def test_defaulting_to_en_language():
    """Test wrong language set in parameter - defaults to en-US."""
    params = {"language": "invalid_language"}
    response = get_top_rated_movies(params=params)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    response_json = response.json()
    first_movie_title_language = detect(response_json["results"][0]["title"])
    first_movie_overview_language = detect(response_json["results"][0]["overview"])

    assert first_movie_title_language == 'en', "Title contains characters that are not en-US"
    assert first_movie_overview_language == 'en', "Overview contains characters that are not en-US"

@pytest.mark.parametrize("language_param, expected_language", [
    ('pl-PL', 'pl'),
    ('en-EN', 'en'),
    ('nl-NL', 'nl'),
])
def test_language_parameter(language_param, expected_language):
    """Test language set in parameter and overview language in response."""
    params = {"language": language_param}
    response = get_top_rated_movies(params=params)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    response_json = response.json()
    first_movie_overview_language = detect(response_json["results"][0]["overview"])

    assert first_movie_overview_language == expected_language, f"Expected overview in {expected_language}, but got {first_movie_overview_language}"

def test_not_found_response():
    """Test a non-existent API endpoint."""
    wrong_endpoint = "https://api.themoviedb.org/3/movie/non_existent_endpoint"
    response = get_top_rated_movies(base_url=wrong_endpoint)
    assert response.status_code == 404, f"Expected 404, got {response.status_code}"

def test_bad_request():
    """Test a 400 Bad Request scenario by omitting required parameters."""
    params = {"language": "en-US"}
    response = get_top_rated_movies(token=None, params=params)
    assert response.status_code in [400, 401], f"Expected 400 or 401, got {response.status_code}"


@pytest.mark.parametrize("page_number", [1, 50, 100])
def test_pagination(page_number):
    """Test pagination"""
    params = {"page": page_number}
    response = get_top_rated_movies(params=params)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    response_json = response.json()
    assert response_json["page"] == page_number, f"Expected page {page_number}, got {response_json['page']}"

    total_pages = response_json["total_pages"]
    assert total_pages > 1, f"Expected more than one total page, but got {total_pages}"

@pytest.mark.parametrize("page_number", [0, 'aaa', 100000])
def test_invalid_page_parameter_message(page_number):
    """Test invalid page query parameter"""
    params = {"page": page_number}
    response = get_top_rated_movies(params=params)
    assert response.status_code == 400, f"Expected 400, got {response.status_code}"

    response_json = response.json()
    assert response_json["status_message"] == INVALID_PAGE_MESSAGE

def test_top_rated_movies_schema():
    """Test response schema"""
    response = get_top_rated_movies()
    try:
        jsonschema.validate(instance=response.json(), schema=TOP_RATED_MOVIES_SCHEMA)
    except jsonschema.exceptions.ValidationError as e:
        pytest.fail(f"Response body does not match schema: {e.message}")
