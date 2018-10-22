from Lecture import Lecture
from html.parser import HTMLParser
from States import States
import re, copy   # Regular expressions

currentState = States.START
currentLecture = Lecture("", "", "", "", "")
currentDate = ""
Lectures = []


class StuVParser:
    def __init__(self, html: str):
        self.html = html

    def parse(self):
        parser = InternalParser()
        parser.feed(self.html)
        return Lectures


class InternalParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        global currentState
        if (currentState == States.LASTSYNCHRONIZED):
            if(tag == "td"):
                for name, value in attrs:
                    if (name == 'colspan' and value == "4"):
                        currentState = States.DATE
        elif (currentState == States.TIME):
            for name, value in attrs:
                if (name == 'colspan' and value == "4"):
                    currentState = States.DATE

    def handle_data(self, data):
        global currentState, currentDate, currentLecture, Lectures
        if(currentState == States.START):
            if(data.startswith("Vorlesungen zuletzt synchronisiert:")):
                print(data)
                currentState = States.LASTSYNCHRONIZED
        elif (currentState == States.LASTSYNCHRONIZED):
            print("Data: States.LASTSYNCHRONIZED" + data)
        elif (currentState == States.DATE):
            match = re.search('(3[01]|[12][0-9]|0[1-9])\.(1[012]|0?[1-9])\.((?:19|20)\d{2})', data)
            if(match != None):
                currentDate = match.group(0)
        elif (currentState == States.TIME):
            startTimeString = data[:5]
            endTimeString = data[-5:]
            matchStartTime = re.search('(00|0[0-9]|1[0-9]|2[0-3]):(0[0-9]|[0-5][0-9])', startTimeString)
            matchEndTime = re.search('(00|0[0-9]|1[0-9]|2[0-3]):(0[0-9]|[0-5][0-9])', endTimeString)
            if(matchStartTime != None and matchEndTime != None):
                startTime = currentDate[-4:] + "-" + currentDate[3:5] + "-" + currentDate[:2] + "T" + matchStartTime.group(0)
                endTime = currentDate[-4:] + "-" + currentDate[3:5] + "-" + currentDate[:2] + "T" + matchEndTime.group(0)
                currentLecture.startTime = startTime
                currentLecture.endTime = endTime
        elif (currentState == States.NAME):
            currentLecture.name = data
        elif (currentState == States.LECTURER):
            currentLecture.lecturer = data
        elif (currentState == States.ROOM):
            currentLecture.room = data
            #print("Lecture: " + currentLecture.name + ", " + currentLecture.lecturer + ", " + currentLecture.room + ", " + currentLecture.startTime + ", " + currentLecture.endTime)
            Lectures.append(copy.copy(currentLecture))

    def handle_endtag(self, tag):
        global currentState
        if (currentState == States.LASTSYNCHRONIZED and tag == "p"):
            currentState = States.DATE
        elif (currentState == States.DATE and tag == "td"):
            currentState = States.TIME
        elif (currentState == States.TIME and tag == "td"):
            currentState = States.NAME
        elif (currentState == States.NAME and tag == "td"):
            currentState = States.LECTURER
        elif (currentState == States.LECTURER and tag == "td"):
            currentState = States.ROOM
        elif (currentState == States.ROOM and tag == "td"):
            currentState = States.TIME
