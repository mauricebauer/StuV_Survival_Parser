from Lecture import Lecture
from ICalExporter import ICalExporter
from StuVParser import StuVParser
import sys
from urllib.request import Request, urlopen

course = 'INF17A'  # Default value of course

if __name__ == "__main__":
    if(len(sys.argv) <= 1):
        print("No command line parameter detected, assuming '" + course + "'")
    else:
        print("Using course: " + sys.argv[1])
        course = sys.argv[1]

    req = Request(
        "https://stuv-mosbach.de/survival/index.php?main=8&course=" + course)
    # Necessary, because insted python is blocked
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)')
    resp = urlopen(req).read()  # Contains the HTML as String
    respUnicode = resp.decode("utf-8")

    parser = StuVParser(respUnicode)
    lectures = parser.parse()  # List holding the lecture objects
    # Clear duplicated lectures with slightly different room
    for currentLecture in lectures:
        for otherLecture in lectures:
            if (otherLecture.startTime == currentLecture.startTime and otherLecture.endTime == currentLecture.endTime and otherLecture.name == currentLecture.name and otherLecture != currentLecture):
                currentLecture.room += (", " + otherLecture.room)
                lectures.remove(otherLecture)
        print("Lecture: " + currentLecture.name + ", " + currentLecture.lecturer + ", " + currentLecture.room + ", " + currentLecture.startTime + ", " + currentLecture.endTime)

    exporter = ICalExporter(lectures)
    exporter.exportICS('calendar.ics')
