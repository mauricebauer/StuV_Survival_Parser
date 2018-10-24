from datetime import datetime
from Lecture import Lecture
from ICalExporter import ICalExporter
from StuVParser import StuVParser
from GoogleCalendarAPI import GoogleCalendarAPI
from urllib.request import Request, urlopen
import dateutil.parser
import sys


course = 'INF17A'  # Default value of course
onlyFutureLectures = True  # Default value of onlyFutureLectures

if __name__ == "__main__":
    scriptStart = datetime.now()
    if(len(sys.argv) <= 1):
        print(str(datetime.now()) + " - No command line parameter detected, assuming '" + course + "' and synchonising only future lectures.")
    else:
        print(str(datetime.now()) + " - Using course: " + sys.argv[1])
        course = sys.argv[1]
        onlyFutureLectures = sys.argv[2]

    req = Request(
        "https://stuv-mosbach.de/survival/index.php?main=8&course=" + course)
    # Necessary, because insted python is blocked
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)')
    resp = urlopen(req).read()  # Contains the HTML as String
    respUnicode = resp.decode("utf-8")

    parser = StuVParser(respUnicode)
    lectures = parser.parse()  # List holding the lecture objects

    # Delete previous lectures
    print(str(datetime.now()) + ' - Deleting previous lectures...')
    GoogleCalendarAPI.deletePrevEvents(onlyFutureLectures, scriptStart)

    # Clear duplicated lectures with slightly different room
    print(str(datetime.now()) + ' - Removing duplicates...')
    for currentLecture in lectures:
        for otherLecture in lectures:
            if (otherLecture.startTime == currentLecture.startTime and otherLecture.endTime == currentLecture.endTime and otherLecture.name == currentLecture.name and otherLecture.room != currentLecture.room):
                currentLecture.room += (", " + otherLecture.room)
                lectures.remove(otherLecture)

    # Remove past lectures (if wanted)
    if (onlyFutureLectures):
        print(str(datetime.now()) + ' - Removing past lectures...')
        for currentLecture in lectures[:]:
            lectureStartTime = dateutil.parser.parse(currentLecture.startTime)
            if (lectureStartTime < scriptStart):
                lectures.remove(currentLecture)

    # Clear duplicated lectures with slightly different room
    print(str(datetime.now()) + ' - Adding lectures...')
    for currentLecture in lectures:
        GoogleCalendarAPI.addEvent(currentLecture)

    #exporter = ICalExporter(lectures)
    #exporter.exportICS('calendar.ics')

    scriptEnd = datetime.now()
    print(str(datetime.now()) + ' - Finished Synchonisation in ' + str(scriptEnd - scriptStart) + '[HH:MM:SS:MsMs]')
