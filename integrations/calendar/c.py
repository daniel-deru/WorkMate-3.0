from datetime import timedelta
import os.path
import tzlocal
import io
import shutil


from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from googleapiclient.errors import HttpError

from utils.globals import PATH

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/drive']


class Google:
    def connect():
        """Shows basic usage of the Google Calendar API.
            Prints the start and name of the next 10 events on the user's calendar.
        """
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(f'{PATH}/integrations/token.json'):
            creds = Credentials.from_authorized_user_file(f'{PATH}/integrations/token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    f'{PATH}/integrations/client_secret_dev.json', SCOPES)
                creds = flow.run_local_server(port=0)
                
            # Save the credentials for the next run
            with open(f'{PATH}/integrations/token.json', 'w') as token:
                token.write(creds.to_json())
    
    def save(date):
        """Shows basic usage of the Google Calendar API.
            Prints the start and name of the next 10 events on the user's calendar.
    """
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(f'{PATH}/integrations/token.json'):
            creds = Credentials.from_authorized_user_file(f'{PATH}/integrations/token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    f'{PATH}/integrations/client_secret_dev.json', SCOPES)
                creds = flow.run_local_server(port=0)
                
            # Save the credentials for the next run
            with open(f'{PATH}/integrations/token.json', 'w') as token:
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
            
    def upload_backup():
        """Shows basic usage of the Google Calendar API.
        Prints the start and name of the next 10 events on the user's calendar.
        """
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(f'{PATH}/integrations/token.json'):
            creds = Credentials.from_authorized_user_file(f'{PATH}/integrations/token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    f'{PATH}/integrations/client_secret_dev.json', SCOPES)
                creds = flow.run_local_server(port=0)
                
            # Save the credentials for the next run
            with open(f'{PATH}/integrations/token.json', 'w') as token:
                token.write(creds.to_json())
        
        try:
            service = build("drive", "v3", credentials=creds)
                      
            files = []
            page_token = None
            while True:
                response = service.files().list(q="mimeType='application/octet-stream'").execute()
                files.extend(response.get('files', []))
                page_token = response.get("nextPageToken", None)
                if page_token == None: break
            

            file_id: str or None = None
            file_exists: bool = False
            for file in files:
                if "name" in file and file['name'] == "workmate.db":
                    file_id = file['id']
                    file_exists = True
                    break
            
            if file_exists:
                service.files().delete(fileId=file_id).execute()

            file_metadata = {'name': 'workmate.db'}
            media = MediaFileUpload('./database/test.db', mimetype='application/octet-stream')
            file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
            # return True
            
        except HttpError as error:
            print('An error occurred: %s' % error)
            
    def download_backup():
        """Shows basic usage of the Google Calendar API.
        Prints the start and name of the next 10 events on the user's calendar.
        """
        print("inside the google download method")
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(f'{PATH}/integrations/token.json'):
            creds = Credentials.from_authorized_user_file(f'{PATH}/integrations/token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    f'{PATH}/integrations/client_secret_dev.json', SCOPES)
                creds = flow.run_local_server(port=0)
                
            # Save the credentials for the next run
            with open(f'{PATH}/integrations/token.json', 'w') as token:
                token.write(creds.to_json())
        
        try:
            service = build("drive", "v3", credentials=creds)
            
            files = []
            page_token = None
            while True:
                response = service.files().list(q="mimeType='application/octet-stream'").execute()
                files.extend(response.get('files', []))
                page_token = response.get("nextPageToken", None)
                if page_token == None: break
                
                
            file_id: str or None = None    
            for file in files:
                if "name" in file and file['name'] == "workmate.db":
                    file_id = file['id']
            
            file = service.files().get_media(fileId=file_id)
            
            download = io.BytesIO()
            downloader = MediaIoBaseDownload(download, file)
            done = False
            
            while not done:
                status, done = downloader.next_chunk()
                print(f"Download {int(status.progress() * 100)}%")
            
            download.seek(0)
            name = "test.db"
            with open(name, "wb") as f:
                shutil.copyfileobj(download, f)
            
            return name
            
        except HttpError as error:
            print('An error occurred: %s' % error)





