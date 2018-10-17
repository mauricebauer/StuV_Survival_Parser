from Lecture import Lecture
from html.parser import HTMLParser

class StuVParser:
    def __init__(self, html: str):
        self.html = html

    def parse(self):
        parser = InternalParser()
        parser.feed(self.html)
        lec1 = Lecture("Testvorlesung", "A0.100", "Dr. Kohlmüller",
                       "2018-10-17T10:58:47+02:00", "2018-10-17T12:58:47+02:00")
        return [lec1]

class InternalParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print("Starttag: " + tag)

    def handle_data(self, data):
        print("Data: " + data)