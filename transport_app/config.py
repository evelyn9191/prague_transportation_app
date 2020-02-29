import os

SQLALCHEMY_DATABASE_URI = os.getenv("SQL_DATABASE_URI", "sqlite:///..\\transport.db",)
SQLALCHEMY_TRACK_MODIFICATIONS = False
