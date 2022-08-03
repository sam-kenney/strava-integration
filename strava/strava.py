"""Module to get data from the Strava API."""
from __future__ import annotations

import typing

import requests

import strava.authentication as authentication


class Strava:
    """Extract data from the Strava API."""

    def __init__(self):
        """Get data from Strava."""
        self.token = authentication.StravaAuthentication().get_token()
        self.headers = {"Authorization": "Bearer " + self.token}

    def get_activities(self) -> typing.List[typing.Dict[str, typing.Any]] | typing.List:
        """Get a list of the user's activities from Strava."""
        url = "https://www.strava.com/api/v3/athlete/activities"
        if response := requests.get(url, headers=self.headers) == 200:
            return response.json()
        return []
