from datetime import datetime, timedelta
import os.path
import tzlocal


from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']


class Google_calendar:
    def connect():
        """Shows basic usage of the Google Calendar API.
            Prints the start and name of the next 10 events on the user's calendar.
        """
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('./integrations/calendar/token.json'):
            creds = Credentials.from_authorized_user_file('./integrations/calendar/token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    './integrations/calendar/client_secret_dev.json', SCOPES)
                creds = flow.run_local_server(port=0)
                
            # Save the credentials for the next run
            with open('./integrations/calendar/token.json', 'w') as token:
                token.write(creds.to_json())
        
        # try:
        #     now = datetime().now()
        #     date = datetime(now.year, now.month, now.day, now.hour, now.minute, now.second)
        #     service = build('calendar', 'v3', credentials=creds)
        #     start_date = date
        #     end_date = start_date + timedelta(minutes=5)
        #     timezone = str(tzlocal.get_localzone())
            
        #     event = {
        #         'summary': 'You connected Google Calendar with WorkMate',
        #         'start': {
        #             'dateTime': start_date.strftime("%Y-%m-%dT%H:%M:%S"),
        #             'timeZone': timezone,
        #         },
        #         'end': {
        #             'dateTime': end_date.strftime("%Y-%m-%dT%H:%M:%S"),
        #             'timeZone': timezone,
        #         },
        #     }

        #     event = service.events().insert(calendarId='primary', body=event).execute()
        # except HttpError as error:
        #     print('An error occurred: %s' % error)
    
    def save(date):
        """Shows basic usage of the Google Calendar API.
            Prints the start and name of the next 10 events on the user's calendar.
    """
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('./integrations/calendar/token.json'):
            creds = Credentials.from_authorized_user_file('./integrations/calendar/token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    './integrations/calendar/client_secret_dev.json', SCOPES)
                creds = flow.run_local_server(port=0)
                
            # Save the credentials for the next run
            with open('./integrations/calendar/token.json', 'w') as token:
                token.write(creds.to_json())
        
        try:
            service = build('calendar', 'v3', credentials=creds)
            start_date = date + timedelta(hours=1)
            end_date = start_date + timedelta(hours=4)
            timezone = str(tzlocal.get_localzone())
            
            event = {
                'summary': 'test',
                'start': {
                    'dateTime': start_date.strftime("%Y-%m-%dT%H:%M:%S"),
                    'timeZone': timezone,
                },
                'end': {
                    'dateTime': end_date.strftime("%Y-%m-%dT%H:%M:%S"),
                    'timeZone': timezone,
                },
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 10},
                    ],
                },
            }

            event = service.events().insert(calendarId='primary', body=event).execute()
            
        except HttpError as error:
            print('An error occurred: %s' % error)





