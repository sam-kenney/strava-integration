"""Module to handle authorisation for Strava API."""
from __future__ import annotations

import os
import webbrowser


class StravaAuthorisation:
    """Handle Strava authorisation for first time users."""

    @staticmethod
    def authorise() -> str:
        """Get authorisation code from Strava."""
        client_id = str(os.environ["STRAVA_CLIENT_ID"])
        print(client_id)
        auth_url = (
            "https://www.strava.com/oauth/authorize?"
            + f"client_id={client_id}&response_type=code&"
            + "redirect_uri=http://localhost/exchange_token"
            + "&approval_prompt=force&scope=activity:read_all"
        )
        print(auth_url)
        webbrowser.open(auth_url)
        resp_url = input(
            "After approving the app, paste the url you were redirected to: "
        )
        return StravaAuthorisation.parse_url(resp_url)

    @staticmethod
    def parse_url(url) -> str:
        """Parse the authorisation code from the url."""
        code = url.split("code=")[1].split("=")[0]
        return code
