"""Main executable file."""
from __future__ import annotations

import os
from datetime import datetime

from cloud_storage_manager import CloudStorage

from strava import Strava


def main() -> None:
    """Entry Point."""
    cs = CloudStorage(default_bucket=os.environ["GCP_BUCKET"])

    cs.download_file(
        gcs_file_name="refresh.txt",
        destination_file_path="/tmp/refresh.txt",
    )

    if data := Strava().get_activities() != []:
        now = str(datetime.now())

        cs.upload_ndjson(
            data=[{**row, "_UPDATED_AT": now} for row in data],
            file_name=f"{now}-strava-activities.ndjson",
        )

    else:
        print("No data found.")

    cs.upload_file(
        file_name="refresh.txt",
    )


if __name__ == "__main__":
    main()
