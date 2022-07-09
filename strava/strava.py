"""Module to get data from the Strava API."""
from __future__ import annotations

import requests

from strava.authentication import StravaAuthentication


class Strava:
    """Extract data from the Strava API."""

    def __init__(self):
        """Get data from Strava."""
        self.token = StravaAuthentication().get_token()
        self.headers = {"Authorization": "Bearer " + self.token}

    def get_activities(self):
        """Get a list of the user's activities from Strava."""
        url = "https://www.strava.com/api/v3/athlete/activities"
        response = requests.get(url, headers=self.headers)
        return response.json()
