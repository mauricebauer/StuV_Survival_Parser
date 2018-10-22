from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import datetime


# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/calendar'
CALENDARID = 'huqusdff4jte5j3dubd343ikmo@group.calendar.google.com'

class GoogleCalendarAPI:

    def deletePrevEvents():
        global CALENDARID, SCOPES
        store = file.Storage('token.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
            creds = tools.run_flow(flow, store)
        service = build('calendar', 'v3', http=creds.authorize(Http()))

        # Searches every event in CALENDARID and deletes it
        page_token = None
        while True:
            events = service.events().list(calendarId=CALENDARID, pageToken=page_token).execute()
            for event in events['items']:
                service.events().delete(calendarId=CALENDARID, eventId=event['id']).execute()
            page_token = events.get('nextPageToken')
            if not page_token:
                break

    def addEvent(lectureEvent):
        global CALENDARID, SCOPES
        store = file.Storage('token.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
            creds = tools.run_flow(flow, store)
        service = build('calendar', 'v3', http=creds.authorize(Http()))

        event = {
          'summary': lectureEvent.name,
          'location': lectureEvent.room,
          'description': 'Dozent: ' + lectureEvent.lecturer,
          'start': {
            'dateTime': lectureEvent.startTime + ":00",
            'timeZone': 'Europe/Berlin',
          },
          'end': {
            'dateTime': lectureEvent.endTime + ":00",
            'timeZone': 'Europe/Berlin',
          },
          'reminders': {
            'useDefault': False,
            'overrides': [
              {'method': 'popup', 'minutes': 60},
            ],
          },
        }

        event = service.events().insert(calendarId=CALENDARID, body=event).execute()
