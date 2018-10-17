from Lecture import Lecture  # Lecture object
from datetime import datetime
from icalendar import Calendar, Event
import dateutil.parser

# lectures is a list of lecture objects


class ICalExporter:
    def __init__(self, lectures):
        self.lectures = lectures

    def exportICS(self, filename: str):
        cal = Calendar()
        for lec in self.lectures:
            event = Event()
            event.add('summary', lec.name)
            event.add('dtstart', dateutil.parser.parse(lec.startTime))
            event.add('dtend', dateutil.parser.parse(lec.endTime))
            event.add('location', lec.room)
            event.add('description', "Dozent: " + lec.lecturer)
            cal.add_component(event)
        f = open(filename, 'wb')
        f.write(cal.to_ical())
        f.close()
