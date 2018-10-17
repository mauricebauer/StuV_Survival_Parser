from Lecture import Lecture
from html.parser import HTMLParser


class StuVParser:
    def __init__(self, html: str):
        self.html = html

    def parse(self):
        lec1 = Lecture("Testvorlesung", "A0.100", "Dr. Kohlmüller",
                       "2018-10-17T10:58:47+02:00", "2018-10-17T12:58:47+02:00")
        return [lec1]
