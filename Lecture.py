# startTime and endTime are Strings for date + time in ISO String Format
class Lecture:
    def __init__(self, name: str, room: str, lecturer: str, startTime: str, endTime: str):
        self.name = name
        self.room = room
        self.lecturer = lecturer
        self.startTime = startTime
        self.endTime = endTime