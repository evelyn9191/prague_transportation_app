import os
from pathlib import Path

SQLALCHEMY_DATABASE_URI = os.getenv("SQL_DATABASE_URI", "sqlite:///..\\transport.db",)
SQLALCHEMY_TRACK_MODIFICATIONS = False

ROOT_DIR = Path(__file__).absolute().parents[1]

TRANSPORT_DATA_URL = "http://data.pid.cz/PID_GTFS.zip"
TRANSPORT_DATA_ZIP = ROOT_DIR / "data" / "PID_GTFS.zip"
LOGS = ROOT_DIR / ".logs"
ZIP_DOWNLOAD_LOG = LOGS / "zip_downloads.log"
LOG_TIME_FORMAT = "%Y-%m-%d"
