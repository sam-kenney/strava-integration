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

    client = Strava()

    now = str(datetime.now())

    data = client.get_activities()
    updated = []

    for row in data:
        row["_UPDATED_AT"] = now
        updated.append(row)

    cs.upload_ndjson(
        data=updated,
        file_name=f"{now}-strava-activities.ndjson",
    )

    cs.upload_file(
        file_name="refresh.txt",
    )


if __name__ == "__main__":
    main()
