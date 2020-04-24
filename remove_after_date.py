"""
helper file
"""
from datetime import datetime

from decouple import config

from caldav_uploader import CalendarDAV

caldav_calendar = CalendarDAV(config('CALENDAR_URL'), config('CALENDAR_USERNAME'), config('CALENDAR_PASSWORD'),
                              config('CALENDAR_NAME'))
results = caldav_calendar.calendar.date_search(datetime(2020, 1, 22), datetime(2021, 6, 1))
for e in results:
    # caldav_calendar.delete(e)
    e.delete()
#    print(e)
