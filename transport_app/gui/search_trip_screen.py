import datetime

import pytz
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty, ListProperty, BooleanProperty, StringProperty
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.screenmanager import (
    ScreenManager,
    Screen,
    NoTransition,
)
from kivy.uix.textinput import TextInput

from transport_app.models import SearchInput
from transport_app.search_database import match_stop

# TODO: redo the datepicker.py to a nice code, PR to kivy garden or something similar
from transport_app.gui.datepicker import DatePicker

Builder.load_file("search_trip_screen.kv")


class TransportSearchApp(App):
    def build(self):
        screen_manager = ScreenManager(transition=NoTransition())
        screen_manager.add_widget(TripSearchScreen(name="search_trip_screen"))
        return screen_manager


class TripSearchScreen(Screen):
    pass


class TransportModes(BoxLayout):
    @staticmethod
    def get_excluded_modes(modes_list: list):
        if all(modes_list):
            return []

        excluded_modes = []

        for order, value in enumerate(modes_list):
            if not value:
                excluded_modes.append(order)
        return excluded_modes

    @classmethod
    def show_error(cls, error_message: str):
        error_popup = ErrorPopup(error_message)
        error_popup.open()


class LowFloorLines(BoxLayout):
    pass


class TravelTime(BoxLayout):
    dept_time = ObjectProperty()
    arr_time = ObjectProperty()

    @classmethod
    def show_error(cls, error_message: str):
        error_popup = ErrorPopup(error_message)
        error_popup.open()


class OneChoiceRadioButton(CheckBox):
    allow_no_selection = BooleanProperty(False)


class TripTime(BoxLayout):
    def get_current_time(self):
        return datetime.datetime.now(tz=pytz.timezone("Europe/Prague")).strftime("%H:%M")


class TransferCountsDropdownMenu(BoxLayout):
    pass


class Header(BoxLayout):
    pass


class MatchedStops(BoxLayout):
    stops_data = ListProperty([])
    departure_stop_name = ObjectProperty()
    stop_name = StringProperty()

    def find_stop(self, stop: str) -> None:
        matched_stops = match_stop(stop)
        self.stops_data = matched_stops

    def fill_departure_stop_name(self, dept_stop_name):
        self.ids.departure_stop.text = dept_stop_name

    def fill_arrival_stop_name(self, arr_stop_name):
        self.ids.arrival_stop.text = arr_stop_name


class StopsList(RecycleView):
    selected = ObjectProperty(None, allownone=True)


class SelectableRecycleGridLayout(FocusBehavior, LayoutSelectionBehavior, RecycleGridLayout):
    """ Adds selection and focus behaviour to the view. """


class SelectableLabel(RecycleDataViewBehavior, Label):
    """Add selection support to the Label"""

    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        """Catch and handle the view changes"""
        self.index = index
        return super(SelectableLabel, self).refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        """Add selection on touch down"""
        if super(SelectableLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        """Respond to the selection of items in the view."""
        self.selected = is_selected
        if is_selected and rv.data[index]["text"] != "None":  # TODO: cover this somewhere
            # matched_stops = MatchedStops()
            # matched_stops.departure_stop_name = rv.data[index]["text"]
            # print(matched_stops.departure_stop_name)
            # DepartureStopName.stop_name_chosen = True
            # DepartureStopName.text = rv.data[index]["text"]
            # departure_stop.stop_name_chosen = True
            departure_stop = DepartureStopName()
            departure_stop.update_changes(rv.data[index]["text"])
            # departure_stop.text = rv.data[index]["text"]
            # MatchedStops().stop_name = rv.data[index]["text"]


class TravelDate(DatePicker):
    @classmethod
    def show_error(cls, error_message: str):
        error_popup = ErrorPopup(error_message)
        error_popup.open()


class ErrorPopup(Popup):
    error_message = StringProperty()

    def __init__(self, error_message, **kwargs):
        super().__init__(**kwargs)
        self.error_message = error_message


class DepartureStopName(TextInput):
    stop_name = StringProperty()
    stop_name_chosen = BooleanProperty(False)
    errors = BooleanProperty(False)

    @classmethod
    def update_changes(cls, stop_name):
        cls.stop_name_chosen = True
        cls.stop_name = stop_name

    @classmethod
    def show_error(cls, error_message: str):
        cls.errors = True
        cls.background_normal = "required_field.png"
        cls.background_active = "required_field.png"
        error_popup = ErrorPopup(error_message)
        error_popup.open()

    @classmethod
    def dismiss_error(cls, error_message: str):
        # cls.errors = True
        # cls.background_normal = 'red.png'
        # cls.background_active = 'red.png'
        # error_popup = ErrorPopup(error_message)
        # error_popup.open()
        pass


class ArrivalStopName(TextInput):
    stop_name = StringProperty()
    stop_name_chosen = BooleanProperty(False)
    updated_text = StringProperty()

    @classmethod
    def update_changes(cls, stop_name):
        cls.stop_name_chosen = True
        cls.stop_name = stop_name

    @classmethod
    def show_error(cls, error_message: str):
        error_popup = ErrorPopup(error_message)
        error_popup.open()


class SearchButton(Button):
    def disable(self):
        self.text = "Searching..."
        self.disabled = True

    def update(self):
        self.text = "Search"
        self.disabled = False

    def start_search(
        self,
        departure_stop,
        arrival_stop,
        time_string,
        travel_date,
        departure_time,
        arrival_time,
        stop_included,
        transfer_counts,
        excluded_travel_modes,
        low_floor_lines_only,
    ):
        user_input = SearchInput(
            departure_stop,
            arrival_stop,
            time_string,
            travel_date,
            departure_time,
            arrival_time,
            stop_included,
            transfer_counts,
            excluded_travel_modes,
            low_floor_lines_only,
        )
        if not user_input.validated_without_errors:
            print("Did not pass validations")
            for error in user_input.error_messages:
                search_button = SearchButton()
                search_button.update()
                instance = _get_class_name(error.field_name)()
                instance.show_error(error.error_message)
        if user_input.validated_without_errors:
            print("Passed validations")


def _get_class_name(field_name: str):
    return {
        "time": TravelTime,
        "departure_stop": DepartureStopName,
        "arrival_stop": ArrivalStopName,
        "transportation_modes": TransportModes,
        "travel_date": TravelDate,
    }.get(field_name, "")


if __name__ == "__main__":
    TransportSearchApp().run()
