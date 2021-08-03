from event import Event
from datetime import datetime


class BaseDriver:

    def get_events_after_date(self, start_date: datetime) -> [Event]:
        pass

    def add_event(self, event: Event):
        pass
