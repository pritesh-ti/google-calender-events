import google.oauth2.credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from google.auth.exceptions import RefreshError

# Set the scope of access to Google Calendar API
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

# Set the path of the credentials file
CREDS_FILE = 'client_secret.json'
CALENDAR_ID = "shantilal@taglineinfotech.com"
EMAILS = set()


def get_refresh_token():
    # Run the authentication flow to get the credentials
    flow = InstalledAppFlow.from_client_secrets_file(CREDS_FILE, SCOPES)
    refresh_token_creds = flow.run_local_server(port=5000)

    # Print the access token for verification
    print(f"Access token: {refresh_token_creds.token}")
    return refresh_token_creds.token


# Set up the credentials object with your client ID, client secret, and refresh token
creds = google.oauth2.credentials.Credentials.from_authorized_user_info(
    info={
        "client_id": "158007534464-uctdj1kj5u7sjkkhe5m1g9okafpi86ql.apps.googleusercontent.com",
        "client_secret": "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",
        "refresh_token": get_refresh_token()
    }
)

# Set up the Calendar API client
calendar_api = build('calendar', 'v3', credentials=creds)

# Retrieve the event with attendee data
try:
    # Retrieve the events for the specified time period
    events_result = calendar_api.events().list(
        calendarId=CALENDAR_ID,
    ).execute()

    # Get the list of events from the API response
    events = events_result.get('items', [])

    # Iterate over each event and print the attendees' email addresses
    for event in events:
        print(event)
        # Check if the event has any attendees
        if 'attendees' in event:
            # Iterate over each attendee and print their email address
            for attendee in event['attendees']:
                if 'email' in attendee:
                    EMAILS.add(attendee["email"])
except HttpError as error:
    print(f"An error occurred: {error}")


print(EMAILS)
