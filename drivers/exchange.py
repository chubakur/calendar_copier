from exchangelib import Credentials, Account, EWSDateTime
from datetime import datetime, timedelta
from drivers import BaseDriver
from event import Event
import dateutil.parser


class ExchangeDriver(BaseDriver):
    def __init__(self, login, password, email):
        self.credentials = Credentials(login, password)
        self.account = Account(email, credentials=self.credentials, autodiscover=True, locale='en_US')

    @staticmethod
    def dirty_hack(datestr: str) -> str:
        return datestr

    def get_events_after_date(self, start_date: datetime) -> [Event]:
        date = EWSDateTime.from_datetime(start_date)
        end_date = EWSDateTime.from_datetime(start_date + timedelta(weeks=2))
        # calendar_events = self.account.calendar.filter(start__range=(date, end_date))
        calendar_events = self.account.calendar.view(start=date, end=end_date)
        results = []
        for event in calendar_events:
            print(event)
            delta = event.end - event.start
            if delta.days >= 1:
                continue
            start_date = event.start.ewsformat()
            end_date = event.end.ewsformat()
            results.append(Event(event.subject, dateutil.parser.isoparse(ExchangeDriver.dirty_hack(start_date)), dateutil.parser.isoparse(ExchangeDriver.dirty_hack(end_date))))
        return results

