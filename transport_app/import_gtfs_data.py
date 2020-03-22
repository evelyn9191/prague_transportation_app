import json
import logging
import os
from datetime import datetime

import requests
from dateutil import parser
from gtfspy import import_gtfs, gtfs

from transport_app import config

logger = logging.getLogger(__file__)
logging.basicConfig(
    level=logging.INFO,
    format='{"time": "%(asctime)s.%(msecs)03d", '
    '"name": "%(name)s", "level": "%(levelname)s", '
    '"message": "%(message)s"}',
    datefmt=f"{config.LOG_TIME_FORMAT} %H:%M:%S",
)


def get_latest_transport_data() -> bool:
    with open(config.ZIP_DOWNLOAD_LOG) as zip_downloads:
        logs = zip_downloads.readlines()
        if not logs:
            download_traffic_source()
            logger.info("ZIP download success")
            return True
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
            return True
        return False


def download_traffic_source() -> None:
    traffic_file = requests.get(config.TRANSPORT_DATA_URL)
    with open(config.TRANSPORT_DATA_ZIP, "wb") as f:
        f.write(traffic_file.content)


def import_gtfs_data(verbose=True) -> bool:
    import_gtfs.import_gtfs(
        [config.TRANSPORT_DATA_ZIP], config.DB_NAME, print_progress=verbose, location_name="Prague",
    )
    g = gtfs.GTFS(config.DB_NAME)
    g.meta["download_date"] = datetime.today().date()
    return True


if __name__ == "__main__":
    data_updated = get_latest_transport_data()
    if data_updated:
        data_imported = import_gtfs_data()
        logger.debug("Transport data updated.")
        if data_imported:
            os.unlink(config.TRANSPORT_DATA_ZIP)
            logger.debug("Transport data ZIP deleted.")
