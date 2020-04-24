from datetime import datetime

import caldav
import icalendar
from icalendar import Calendar


class CalendarDAV(caldav.DAVClient):
    def __init__(self, url, username, password, name):
        super().__init__(url=url, username=username, password=password)
        self.client = caldav.DAVClient(url=url, username=username, password=password, ssl_verify_cert=False)
        self.calendar = [calendar for calendar in self.principal().calendars() if calendar.name == name][0]

    def is_event_colliding(self, start, end):
        meantime_events = self.calendar.date_search(start, end)
        for calendar_event in meantime_events:
            event = Calendar.from_ical(calendar_event.data).subcomponents[0]
            if "*" in event["SUMMARY"]:
                return True

    def add_event(self, uid, start, end, summary, location, color=None):
        if self.is_event_colliding(start, end):
            return False
        event = icalendar.Event()
        event.add('uid', uid + '@LIBRUS.M4K5.ME')
        event.add('dtstart', start)
        event.add('dtend', end)
        event.add('dtstamp', datetime.now())
        event.add('summary', summary)
        event.add('location', location)
        if color:
            event.add('color', color)
        calendar_for_event = icalendar.Calendar()
        calendar_for_event.add('prodid', 'LIBRUS_SUITE_BY_M4K5')
        calendar_for_event.add('version', '2.0')
        calendar_for_event.add_component(event)
        self.calendar.add_event(calendar_for_event.to_ical())

    def remove_event(self, uid):
        event = self.calendar.event_by_uid(uid + '@LIBRUS.M4K5.ME')
        return event.delete()
