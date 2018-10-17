from Lecture import Lecture
from ICalExporter import ICalExporter

lec1 = Lecture("Testvorlesung", "A0.100", "Dr. Kohlmüller", "2018-10-17T10:58:47+02:00", "2018-10-17T12:58:47+02:00")
lectures = [lec1]

if __name__ == "__main__":
    exporter = ICalExporter(lectures)
    exporter.exportICS('calendar.ics')