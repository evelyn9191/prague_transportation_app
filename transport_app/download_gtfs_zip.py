import json
import logging
from datetime import datetime

import requests
from dateutil import parser

from transport_app import config

logger = logging.getLogger(__file__)
logging.basicConfig(
    level=logging.INFO,
    format='{"time": "%(asctime)s.%(msecs)03d", '
    '"name": "%(name)s", "level": "%(levelname)s", '
    '"message": "%(message)s"}',
    datefmt=f"{config.LOG_TIME_FORMAT} %H:%M:%S",
)


def check_latest_gtfs_zip() -> None:
    with open(config.ZIP_DOWNLOAD_LOG) as zip_downloads:
        logs = zip_downloads.readlines()
        if not logs:
            download_traffic_source()
            logger.info("ZIP download success")
            return None
        last_update = json.loads(logs[-1])
        download_date = parser.parse(last_update["time"])
        today = datetime.today()
        zip_update_time = datetime.strptime("18:00", "%H:%M").time()
        if (
            download_date.date() <= today.date()
            and download_date.time() < zip_update_time < today.time()
        ):
            download_traffic_source()
            logger.info("ZIP download success")
            return None


def download_traffic_source() -> None:
    traffic_file = requests.get(config.TRANSPORT_DATA_URL)
    with open(config.TRANSPORT_DATA_ZIP, "wb") as f:
        f.write(traffic_file.content)


if __name__ == "__main__":
    check_latest_gtfs_zip()
