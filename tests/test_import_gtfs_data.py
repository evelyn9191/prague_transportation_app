import json
import os
from datetime import datetime
from unittest import mock

from freezegun import freeze_time

from tests import MOCK_DATA, MOCK_ZIP_FILE
from transport_app import config
from transport_app.import_gtfs_data import get_latest_transport_data, download_traffic_source

config.TRANSPORT_DATA_URL = "httpmock://gtfs_source.xz"
config.TRANSPORT_DATA_ZIP = MOCK_DATA / "mock_downloaded_gtfs.zip"
config.ZIP_DOWNLOAD_LOG = MOCK_DATA / "mock_log.log"


class TestDownloadNewGTFSZip:
    today = datetime.today().date()
    before_six = "14:00:00.000"
    after_six = "19:00:00.000"

    def test_check_latest_gtfs_zip_first_time_import(self, requests_mock):
        requests_mock.get(
            config.TRANSPORT_DATA_URL, content=MOCK_ZIP_FILE, status_code=200,
        )
        with mock.patch("transport_app.import_gtfs_data.logger") as mock_logger:
            updated_data = get_latest_transport_data()
            mock_logger.info.assert_called_once_with("ZIP download success")
            assert updated_data is True
        os.unlink(config.TRANSPORT_DATA_ZIP)

    @freeze_time(f"{today} {after_six}")
    def test_check_latest_gtfs_zip_imported_already(self):
        last_download = f"{self.today.strftime(config.LOG_TIME_FORMAT)} {self.after_six}"
        create_log(last_download)
        updated_data = get_latest_transport_data()
        self._assert_last_log(last_download)
        assert updated_data is False

    @freeze_time(f"{today} {after_six}")
    def test_check_latest_gtfs_zip_old_import(self, requests_mock):
        last_download = f"{self.today.strftime(config.LOG_TIME_FORMAT)} {self.before_six}"
        requests_mock.get(
            config.TRANSPORT_DATA_URL, content=MOCK_ZIP_FILE, status_code=200,
        )
        create_log(last_download)
        updated_data = get_latest_transport_data()
        self._assert_last_log(last_download)
        assert updated_data is True

        os.unlink(config.TRANSPORT_DATA_ZIP)
        with open(config.ZIP_DOWNLOAD_LOG, "r+") as logs_file:
            logs_file.truncate(0)

    @staticmethod
    def _assert_last_log(last_download: str):
        with open(config.ZIP_DOWNLOAD_LOG) as zip_downloads:
            logs = zip_downloads.readlines()
            last_log = json.loads(logs[-1])
            assert last_log["time"] == last_download


class TestDownloadGTFSZip:
    def test_download_traffic_source(self, requests_mock):
        requests_mock.get(
            config.TRANSPORT_DATA_URL, content=MOCK_ZIP_FILE, status_code=200,
        )
        download_traffic_source()
        assert config.TRANSPORT_DATA_ZIP.exists() is True
        os.unlink(config.TRANSPORT_DATA_ZIP)


def create_log(last_download: str) -> None:
    log_input = (
        f'{{"time": "{last_download}", '
        f'"name": "some/path", '
        f'"level": "INFO", '
        f'"message": "ZIP download success"}}'
    )
    with open(config.ZIP_DOWNLOAD_LOG, "w") as zip_downloads:
        zip_downloads.write(log_input)
