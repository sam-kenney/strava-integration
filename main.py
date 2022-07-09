"""Main executable file."""
from __future__ import annotations

import csv
from datetime import datetime

from strava import Strava


def main() -> None:
    """Entry Point."""
    client = Strava()
    data = client.get_activities()

    headers = [
        "Date",
        "Distance (km)",
        "Avg. Speed (km/h)",
        "Avg. Cadence",
        "Avg. Heart Rate",
    ]

    formatted_data = format_data(data, headers)
    write_data(formatted_data, "strava_data.csv")


def format_data(
    data: list[dict[str, str | int]],
    headers: list[str],
) -> list[list[str]]:
    """Format data to be written to csv file."""
    as_csv = [headers]

    for ride in data:
        row = []

        date = datetime.strptime(
            ride["start_date_local"], "%Y-%m-%dT%H:%M:%SZ"
        ).strftime("%Y-%m-%d")

        row.append(date)
        row.append(round(ride["distance"] / 1000, 2))
        row.append(round(ride["average_speed"] * 3.6, 2))
        row.append(ride["average_cadence"])
        row.append(ride.get("average_heartrate", "n/a"))

        as_csv.append(row)

    return as_csv


def write_data(data: list[list[str]], filename: str):
    """Write data to csv file."""
    with open(filename, "w") as f:
        writer = csv.writer(f)
        writer.writerows(data)


if __name__ == "__main__":
    main()
