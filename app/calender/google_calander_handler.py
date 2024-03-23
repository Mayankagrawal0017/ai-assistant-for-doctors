import time
from datetime import datetime, timedelta
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import utils
# If modifying these scopes, delete the file app/calender/token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]

def get_service():
    creds = None
    if os.path.exists("app/calender/token.json"):
        creds = Credentials.from_authorized_user_file(
            "app/calender/token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "app/calender/credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("app/calender/token.json",
                  "w") as token:
            token.write(creds.to_json())
    service = build("calendar", "v3", credentials=creds)
    return service


def get_schedule(service):
    # Call the Calendar API
    now = datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
    print("Getting the upcoming 10 events")
    events_result = (service.events().list(calendarId="primary", timeMin=now, maxResults=10,
                                           singleEvents=True, orderBy="startTime", ).execute())
    events = events_result.get("items", [])

    if not events:
        print("No upcoming events found.")
        return

    # Prints the start and name of the next 10 events
    for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        print(start, event["summary"])


def create_event(service, event_info):
    start_time = event_info["start_time"]
    end_time = start_time + timedelta(minutes=event_info.get("slot_duration", 30))
    event = {
      'summary': f'Appointment with {event_info["first_name"]}  {event_info.get("last_name")}' if event_info["type"] == "Appointment" else "Calender Block",
      'location': '',
      'description': f'PatentId: {event_info["patent_id"]}\nName: {event_info["first_name"]} {event_info.get("last_name")}\nAge: {utils.calculate_age(event_info.get("date_of_birth"))}\nPhone Number: {event_info.get("phone_number")}\n Email: {event_info.get("email")}\nReason: {event_info.get("reason")}',
      'start': {
        'dateTime': start_time.strftime("%Y-%m-%dT%H:%M:%S"),
        'timeZone': 'UTC',
      },
      'end': {
        'dateTime': end_time.strftime("%Y-%m-%dT%H:%M:%S"),
        'timeZone': 'UTC',
      },
      'reminders': {
        'useDefault': False,
        'overrides': [
          {'method': 'popup', 'minutes': 15},
        ],
      },
    }
    guests = event_info.get('attendees', ["mayank.agrawal.unthinkable@gmail.com"])
    if guests:
        event['attendees'] = [{'email': guest} for guest in guests]
    event = service.events().insert(calendarId='primary', body=event).execute()
    return event.get('status'), event.get('id')


def delete_event(service, event_id):
    try:
        service.events().delete(calendarId='primary', eventId=event_id, sendUpdates='all').execute()
    except HttpError:
        return False, "Failed to delete event"
    else:
        return True, "Event deleted"


if __name__ == "__main__":

    event_info = {
        "start_time":  datetime.utcnow(),
        "first_name": "Mayank",
        "last_name": "Agrawal",
        "type": "Appointment",
        "date_of_birth": "02022000",
        "patent_id": "ADFR",
        "phone_number": "9876543210",
        "email": "mayank.agrawal.unthinkable@gmail.com",
        "reason": "Testing",

    }
    service = get_service()

    status, event_id = create_event(service, event_info)
    get_schedule(service)
    time.sleep(60)
    print(delete_event(service, event_id))



