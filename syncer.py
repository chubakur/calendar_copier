from drivers import BaseDriver
from datetime import datetime
from pytz import timezone


class Syncer:
    def __init__(self, input_calendar: BaseDriver, output_calendar: BaseDriver):
        self.input = input_calendar
        self.output = output_calendar

    @staticmethod
    def find_event(event, events):
        for te in events:
            # print(event, te, event == te)
            if te == event:
                return True
        return False

    def process(self):
        start_date = datetime.now(timezone('Europe/Moscow'))
        events = self.input.get_events_after_date(start_date)
        target_events = self.output.get_events_after_date(start_date)
        for event in events:
            if not Syncer.find_event(event, target_events):
                print('Need ADD ', event)
                self.output.add_event(event.copy())
