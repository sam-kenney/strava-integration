"""Module to handle authentication for Strava API."""
from __future__ import annotations

import os
import requests

from strava.authorisation import StravaAuthorisation


class StravaAuthentication:
    """Class to handle authentication for Strava API."""

    def __init__(self, token_path: str = "/tmp/refresh.txt") -> StravaAuthentication:
        """Class to handle authentication for Strava API."""
        self.client_id = str(os.environ["STRAVA_CLIENT_ID"])
        self.secret = os.environ["STRAVA_CLIENT_SECRET"]
        self.token_path = token_path

    def get_token(self) -> str:
        """Get an access token from Strava."""
        if os.path.isfile(self.token_path):
            return self.refresh_access_token()

        return self.get_new_token()

    def refresh_access_token(self):
        """If a refresh token is available, use it to get a new access token."""
        with open(self.token_path, "r") as f:
            refresh_token = f.read()

        auth_url = (
            "https://www.strava.com/oauth/token"
            + f"?client_id={self.client_id}"
            + f"&client_secret={self.secret}"
            + f"&refresh_token={refresh_token}"
            + "&grant_type=refresh_token"
        )

        response = requests.post(auth_url)
        if response.status_code != 200:
            return self.get_new_token()

        token = response.json()["access_token"]
        self.store_refresh_token(response.json()["refresh_token"])
        return token

    def store_refresh_token(self, refresh_token):
        """Save the refresh token to a file."""
        with open(self.token_path, "w") as f:
            f.write(refresh_token)

    def get_new_token(self):
        """Get a new access token with user authorisation."""
        auth_url = (
            "https://www.strava.com/oauth/token"
            + f"?client_id={self.client_id}"
            + f"&client_secret={self.secret}"
            + f"&code={StravaAuthorisation.authorise()}"
            + "&grant_type=authorization_code"
        )

        response = requests.post(auth_url)
        if response.status_code == 200:
            token = response.json()["access_token"]
            self.store_refresh_token(response.json()["refresh_token"])
            return token

        raise Exception("Failed to get access token")
