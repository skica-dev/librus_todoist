import sys
import pickle
from datetime import datetime, timedelta

import pytz
import todoist
from caldav.lib.error import NotFoundError
from decouple import config
from librus_tricks import create_session

from caldav_uploader import CalendarDAV


class SynergiaSession:
    def __init__(self, username, password):
        # user = authorizer(username, password)[0]
        # super().__init__(user)
        self.session = create_session(username, password)
        self.school_location = self.session.school.location

    def formatted_full_timetable(self):
        ff_timetable = {}
        day = datetime.today()
        while day < datetime(2020, 6, 26):
            timetable = self.session.timetable(for_date=day)
            for i in timetable.days:
                if timetable.days[i].lessons:
                    ff_timetable[i] = timetable.days[i].lessons
            day += timedelta(days=7)
        return ff_timetable


class Timetable2CalDav:
    def __init__(self, synergia_session, calendar):
        self.calendar = calendar
        self.session = synergia_session

    def sync(self, timetable=None):
        if not timetable:
            timetable = self.session.formatted_full_timetable()
        for day in timetable:
            for lesson in timetable[day]:
                try:
                    self.calendar.remove_event("{}_{}".format(lesson.lesson_no, day))
                    print("removed " + str(lesson))
                except NotFoundError:
                    pass
                if lesson.is_cancelled or lesson.subject.name in IGNORED_SUBJECTS:
                    continue
                try:
                    location = (
                        lesson.classroom.name + ", " + self.session.school_location
                    )
                except TypeError:
                    location = self.session.school_location
                self.calendar.add_event(
                    uid="{}_{}".format(lesson.lesson_no, day),
                    start=datetime.combine(
                        day, lesson.start, tzinfo=pytz.timezone("Europe/Warsaw")
                    ),
                    end=datetime.combine(
                        day, lesson.end, pytz.timezone("Europe/Warsaw")
                    ),
                    summary=lesson.subject.name,
                    location=location,
                )
                print("added " + str(lesson))


def last_message_header_pickle(new=None):
    filename = "last_message_header.pickle"
    if new:
        with open(filename, "wb") as fi:
            # dump your data into the file
            return pickle.dump(new, fi)
    try:
        with open(filename, "rb") as fi:
            header = pickle.load(fi)
            return header
    except:
        return "Drodzy Uczniowie"


class Messages2Todoist:
    def __init__(self, synergia_session, todoist):
        self.session = synergia_session.session
        self.todoist = todoist
        self.todoist.sync()

    def sync(self):
        last_message_header = last_message_header_pickle()
        messages = self.session.message_reader.read_messages()
        if len(messages) == 0:
            return
        if messages[0].header != last_message_header:
            for message in messages:
                print(message.header)
                if message.header == last_message_header:
                    self.todoist.commit()
                    last_message_header_pickle(messages[0].header)
                    break
                new_task = self.todoist.items.add(
                    "{} od {}".format(message.header, message.author)
                )
                self.todoist.notes.add(new_task.temp_id, message.text)


def sync_timetable(librus_session):
    caldav_calendar = CalendarDAV(
        config("CALENDAR_URL"),
        config("CALENDAR_USERNAME"),
        config("CALENDAR_PASSWORD"),
        config("CALENDAR_NAME"),
    )
    timetable2caldav = Timetable2CalDav(librus_session, caldav_calendar)
    timetable2caldav.sync()


def sync_messages(librus_session):
    todoist_session = todoist.TodoistAPI(config("TODOIST_API_KEY"))
    messages2todoist = Messages2Todoist(librus_session, todoist_session)
    messages2todoist.sync()


if __name__ == "__main__":
    librus_session = SynergiaSession(
        config("LIBRUS_USERNAME"), config("LIBRUS_PASSWORD")
    )
    try:
        assert sys.argv[1] == "messages"
        sync_messages(librus_session)
    except:
        IGNORED_SUBJECTS = ["wychowanie fizyczne fakultet", "_opieka_WF"]
        sync_timetable(librus_session)
