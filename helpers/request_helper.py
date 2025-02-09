import requests
import configparser
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = BASE_DIR / "config.ini"

config = configparser.ConfigParser()
config.read(CONFIG_PATH)

BASE_URL_TOP_RATED = config["API"]["BASE_URL_TOP_RATED"]
BASE_URL_RATE_MOVIE = config["API"]["BASE_URL_RATE_MOVIE"]

BEARER_TOKEN = os.getenv("BEARER_TOKEN")


def get_top_rated_movies(base_url=BASE_URL_TOP_RATED, token=BEARER_TOKEN, params=None):
    """
    Helper method to send a GET request to get top rated movies.
    :param base_url: base URL to make request
    :param token: API bearer token
    :param params: request parameters
    :return: request response
    """
    if not params:
        params = {}

    headers= {
        "Accept": "application/json",
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(base_url, headers=headers, params=params)
    return response

def rate_movie(movie_id = 402431, rating = 8.5, base_url=BASE_URL_RATE_MOVIE, token=BEARER_TOKEN):
    """
    Helper method to send a POST request to rate movie.
    :param movie_id: ID of movie to rate
    :param rating: rating of a movie
    :param base_url: base URL to make request
    :param token: API bearer token
    :return: request response
    """
    headers= {
        "Accept": "application/json",
        "Authorization": f"Bearer {token}"
    }

    url = base_url.replace('movie_id', str(movie_id))

    payload = {"value": rating}

    response = requests.post(url, data=payload, headers=headers)
    return response
