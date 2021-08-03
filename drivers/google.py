from datetime import datetime
import dateutil.parser

from drivers import BaseDriver
from event import Event
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import os.path
import pickle


class GoogleDriver(BaseDriver):
    SCOPES = ['https://www.googleapis.com/auth/calendar']

    def __init__(self):
        token_filename = 'settings/google_token.pickle'
        self.creds = None
        if os.path.exists(token_filename):
            with open(token_filename, 'rb') as token:
                self.creds = pickle.load(token)
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                self.flow = InstalledAppFlow.from_client_secrets_file('settings/credentials.json', GoogleDriver.SCOPES)
                self.creds = self.flow.run_local_server(port=0)
            with open(token_filename, 'wb') as token:
                pickle.dump(self.creds, token)

        self.service = build('calendar', 'v3', credentials=self.creds)

    def get_events_after_date(self, start_date: datetime) -> [Event]:
        events_result = self.service.events().list(calendarId='primary', timeMin=start_date.isoformat(),
                                        maxResults=1000, singleEvents=True,
                                        orderBy='startTime').execute()
        events = events_result.get('items', [])
        result = []
        for event in events:
            if 'dateTime' in event['start'] and 'dateTime' in event['end']:
                try:
                    ev = Event(event['summary'], dateutil.parser.isoparse(event['start']['dateTime']), dateutil.parser.isoparse(event['end']['dateTime']))
                    result.append(ev)
                except KeyError:
                    continue
        return result

    def add_event(self, event: Event):
        api_event = {
            'summary': event.subject,
            'start': {
                'dateTime': event.start_date.isoformat(),
                'timeZone': 'Europe/Moscow',
                # 'timeZone': 'UTC'
            },
            'end': {
                'dateTime': event.end_date.isoformat(),
                'timeZone': 'Europe/Moscow',
            },
            'reminders': {
                'useDefault': False
            }
        }
        # print(api_event)
        self.service.events().insert(calendarId='primary', body=api_event).execute()
