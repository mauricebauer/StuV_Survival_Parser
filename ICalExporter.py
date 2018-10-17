from Lecture import Lecture  # Lecture object
from datetime import datetime
from icalendar import Calendar, Event
import dateutil.parser


class ICalExporter:
    # lectures is a list of lecture objects
    def __init__(self, lectures):
        self.lectures = lectures

    def exportICS(self, filename: str):
        cal = Calendar()
        cal.add('version', "2.0")
        cal.add('prodid', "StuV_Survival_Parser")
        uid = 0
        for lec in self.lectures:
            event = Event()
            event.add('uid', str(uid))
            event.add('summary', lec.name)
            event.add('dtstart', dateutil.parser.parse(lec.startTime))
            event.add('dtend', dateutil.parser.parse(lec.endTime))
            event.add('dtstamp', datetime.now())
            event.add('location', lec.room)
            event.add('description', "Dozent: " + lec.lecturer)
            cal.add_component(event)
            uid += 1    # Increase the universal id of each event
        f = open(filename, 'wb')
        f.write(cal.to_ical())
        f.close()
