import logging

from .db_models import session, Stops

logger = logging.getLogger(__name__)


def match_stop(stop: str) -> dict:
    matched_stops = (
        session.query(Stops)
        .with_entities(Stops.name)
        .filter(Stops.name.ilike(stop + "%"))
        .group_by(Stops.name)
    ).all()
    return matched_stops
