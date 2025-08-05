import datetime
import os
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Google Calendar API scope
SCOPES = ["https://www.googleapis.com/auth/calendar"]

def get_calendar_service():
    """
    Authenticates and returns a Google Calendar API service object.
    - On the first run, opens a browser window for login.
    - Stores a token.pickle file for future reuse.
    """
    creds = None
    token_file = "token.pickle"
    credentials_path = os.getenv("GOOGLE_CREDENTIALS_PATH")

    if not credentials_path or not os.path.exists(credentials_path):
        raise FileNotFoundError(
            "Missing GOOGLE_CREDENTIALS_PATH or credentials.json file."
        )

    # Load saved token if available
    if os.path.exists(token_file):
        with open(token_file, "rb") as token:
            creds = pickle.load(token)

    # If no valid creds, start the OAuth process
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_path, SCOPES
            )
            creds = flow.run_local_server(port=0)

        # Save credentials for future use
        with open(token_file, "wb") as token:
            pickle.dump(creds, token)

    return build("calendar", "v3", credentials=creds)


def create_event(
    summary: str,
    description: str,
    start_time: datetime.datetime,
    duration_minutes: int = 30,
):
    """
    Creates an event in the user's primary Google Calendar
    and returns the event's HTML link.
    """
    service = get_calendar_service()

    event = {
        "summary": summary,
        "description": description,
        "start": {
            "dateTime": start_time.isoformat(),
            "timeZone": "Asia/Kolkata",
        },
        "end": {
            "dateTime": (
                start_time + datetime.timedelta(minutes=duration_minutes)
            ).isoformat(),
            "timeZone": "Asia/Kolkata",
        },
    }

    created_event = (
        service.events().insert(calendarId="primary", body=event).execute()
    )
    return created_event.get("htmlLink")
