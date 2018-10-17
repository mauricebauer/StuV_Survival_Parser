from Lecture import Lecture
from ICalExporter import ICalExporter
import sys

course = 'INF17A'  # Default value of course
lec1 = Lecture("Testvorlesung", "A0.100", "Dr. Kohlmüller",
               "2018-10-17T10:58:47+02:00", "2018-10-17T12:58:47+02:00")
lectures = [lec1]

if __name__ == "__main__":
    if(len(sys.argv) <= 1):
        print("No command line parameter detected, assuming '" + course + "'")
    else:
        print("Using course: " + sys.argv[1])
        course = sys.argv[1]

    exporter = ICalExporter(lectures)
    exporter.exportICS('calendar.ics')
