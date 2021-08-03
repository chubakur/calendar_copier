from datetime import datetime


class Event:

    def __init__(self, subject: str, start_date: datetime, end_date: datetime):
        self.subject = subject
        self.start_date = start_date
        self.end_date = end_date

    def __repr__(self):
        return "Event({subject}: {start} {end})".format(subject=self.subject, start=self.start_date, end=self.end_date)

    def __eq__(self, other):
        if self.start_date != other.start_date:
            return False
        if self.end_date != other.end_date:
            return False
        xs = self.subject.strip()
        os = other.subject.strip()
        return xs == os or \
               Event.copyName(xs) == os or \
               xs == Event.copyName(os)

    @staticmethod
    def copyName(name: str) -> str:
        return 'SYNC/' + name

    def copy(self):
        return Event(Event.copyName(self.subject), self.start_date, self.end_date)
