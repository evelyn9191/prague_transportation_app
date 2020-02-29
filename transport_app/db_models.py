from typing import Any

from marshmallow import EXCLUDE
from marshmallow_sqlalchemy import ModelSchema
from sqlalchemy import Integer, Column, String, ForeignKey, orm
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as sa

from .config import SQLALCHEMY_DATABASE_URI

AGENCY, CALENDAR, CALENDAR_DATES, ROUTES, SHAPES, STOP_TIMES, STOPS, TRANSFERS, TRIPS = (
    "agency",
    "calendar",
    "calendar_dates",
    "routes",
    "shapes",
    "stop_times",
    "stops",
    "transfers",
    "trips",
)

Base = declarative_base()  # type: Any
engine = sa.create_engine(SQLALCHEMY_DATABASE_URI)
Base.metadata.bind = engine
session = orm.scoped_session(orm.sessionmaker())(bind=engine)

# FIXME: all the models below are outdated. There were used to work with a different solution
#  that did not apply the gtfspy library. They are kept here because:
#  1. the Stops model is used in search_database.py
#  2. StopsVirtual should still substitute the Stops or a new table should be created where
#  indices will be created to make the search faster (but it may not be needed, there are not so many
#  stops, anyway)
#  3. the issue with Czech special chars needs to be solved, so FTS5 may still be needed


class StopsVirtual(Base):
    __tablename__ = "stops_virtual"

    # TODO: primary_key is not being created
    id = Column(Integer, primary_key=True, autoincrement=True)  # noqa: A003
    stop_id = Column(String)
    stop_name = Column(String, ForeignKey("stops.stop_name"))

    def __repr__(self):
        return f"<{self.__class__.__name__}Virtual table Stops: (stop_name={self.stop_id})>"


class StopsVirtualSchema(ModelSchema):
    class Meta:
        unknown = EXCLUDE
        include_fk = True
        model = StopsVirtual
        sqla_session = session


class Stops(Base):
    __tablename__ = "stops"

    id = Column(Integer, primary_key=True, autoincrement=True)  # noqa: A003
    stop_id = Column(String)
    name = Column(String)
    stop_lat = Column(String)
    stop_lon = Column(String)
    zone_id = Column(String)
    stop_url = Column(String)
    location_type = Column(Integer)
    parent_station = Column(String)
    wheelchair_boarding = Column(Integer)
    level_id = Column(Integer)
    platform_code = Column(String)

    def __repr__(self):
        return f"<{self.__class__.__name__}(stop_id={self.stop_id}, stop_name={self.stop_name})>"


def create_tables(engine: Engine):
    engine.execute("CREATE VIRTUAL TABLE stops_virtual USING FTS5(id, stop_id, stop_name)")
    Base.metadata.create_all(engine)
