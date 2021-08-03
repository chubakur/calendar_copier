from datetime import datetime

from drivers import BaseDriver
from event import Event


class PrinterDriver(BaseDriver):

    def get_events_after_date(self, start_date: datetime) -> [Event]:
        return []

    def add_event(self, event: Event):
        print(event)
