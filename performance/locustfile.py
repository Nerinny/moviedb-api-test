import sys
from locust import HttpUser, between, task, events
from helpers.request_helper import BEARER_TOKEN, BASE_URL_TOP_RATED

class TMDBUser(HttpUser):
    wait_time = between(1,3)
    host = BASE_URL_TOP_RATED

    def on_start(self):
        scenario = self.environment.parsed_options.scenario

        if scenario == "burst":
            self.environment.runner.start(user_count=500, spawn_rate=50)
        elif scenario == "staggered":
            self.environment.runner.start(user_count=200, spawn_rate=10)
        else:
            self.environment.runner.start(user_count=300, spawn_rate=20)

    @task
    def get_top_rated_movies(self):
        params = {
            "language": "en-US",
            "page": 1
        }
        headers = {
            "Authorization": f"Bearer {BEARER_TOKEN}",
            "Content-Type": "application/json"
        }

        response = self.client.get("", headers=headers, params=params)

        if response.status_code == 429:
        # TMDB responds with 429 when rate limit
            events.quitting.fire()
            sys.exit(0)

        assert response.status_code == 200, f"Expected 200, but got {response.status_code}"

@events.init_command_line_parser.add_listener
def _(parser):
    parser.add_argument("--scenario", type=str, default="normal", help="Load balancing scenario: normal, burst, or staggered")
