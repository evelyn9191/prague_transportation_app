from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from dateutil import parser


TIME, DEPARTURE_STOP, ARRIVAL_STOP, DATE, TRAVEL_MODES = (
    "time",
    "departure_stop",
    "arrival_stop",
    "travel_date",
    "transportation_modes",
)


@dataclass
class ErrorMessage:
    field_name: str
    error_message: str


class SearchInput:
    def __init__(
        self,
        departure_stop,
        arrival_stop,
        time_string: str,
        travel_date,
        departure_time,
        arrival_time,
        stop_included,
        transfer_counts,
        excluded_travel_modes,
        low_floor_lines_only,
    ):
        self.departure_stop = departure_stop
        self.arrival_stop = arrival_stop
        self.time = time_string
        self.travel_date = travel_date
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.stop_included = stop_included
        self.transfer_counts = transfer_counts
        self.excluded_travel_modes = excluded_travel_modes
        self.low_floor_lines_only = low_floor_lines_only
        self.travel_day = None
        self.error_messages: List[ErrorMessage] = []

        self.sanitize_attributes()

    @property
    def validated_without_errors(self):
        validated_without_errors = True if not self.error_messages else False
        return validated_without_errors

    def sanitize_attributes(self):
        self.departure_stop = self.sanitize_stop_name(
            self.departure_stop, "departure", DEPARTURE_STOP
        )
        self.arrival_stop = self.sanitize_stop_name(self.arrival_stop, "arrival", ARRIVAL_STOP)
        self.time = self.sanitize_time(self.time, TIME)
        self.travel_date = self.sanitize_date(self.travel_date, DATE)
        self.travel_day = self.get_weekday(self.travel_date)
        self.excluded_travel_modes = self.validate_travel_modes(
            self.excluded_travel_modes, TRAVEL_MODES
        )

    def sanitize_stop_name(self, stop_name: str, stop_direction: str, field_name: str):
        if not stop_name:
            error_message = ErrorMessage(
                field_name=field_name, error_message=f"Missing {stop_direction} stop name."
            )
            self.error_messages.append(error_message)

        # TODO: do some sanitizations, if user decides not to choose from a label
        # error_message = ErrorMessage(field_name=field_name, error_message=f'Incorrect {stop_direction} stop name.')
        # self.error_messages.append(error_message)
        return stop_name

    def sanitize_time(self, time: str, field_name: str) -> Optional[str]:
        try:
            formatted_time = parser.parse(time).time().isoformat()
            return formatted_time
        except ValueError:
            error_message = ErrorMessage(
                field_name=field_name, error_message="Incorrect time format."
            )
            self.error_messages.append(error_message)
            return None

    def sanitize_date(self, travel_date: str, field_name: str) -> Optional[str]:
        try:
            trip_date = parser.parse(travel_date).date().isoformat()
            return trip_date
        except ValueError:
            error_message = ErrorMessage(
                field_name=field_name, error_message="Incorrect date format."
            )
            self.error_messages.append(error_message)
            return None

    def validate_travel_modes(self, travel_modes: list, field_name: str) -> list:
        if len(travel_modes) == 5:
            error_message = ErrorMessage(
                field_name=field_name, error_message="At least one mode of travel must be chosen."
            )
            self.error_messages.append(error_message)
        return travel_modes

    @staticmethod
    def get_weekday(date: Optional[str]) -> Optional[int]:
        if not date:
            return None

        return datetime.strptime(date, "%Y-%m-%d").isoweekday()
