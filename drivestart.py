from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']
template = "1kjVTREYQKYW9wagG6v8g-tSdHYDLle5_6MfI1_6uOac"


def get_service():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('creds/drivetoken.pickle'):
        with open('creds/drivetoken.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'creds/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('creds/drivetoken.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('drive', 'v3', credentials=creds)


def copy(docid: str, name: str = "", folderid: str = "", service=None):
    if not service:
        service = get_service()

    data = service.files().copy(fileId=docid, fields="id, parents").execute()

    id = data["id"]
    prevParents = ','.join(data["parents"])

    if name:
        # rename here
        service.files().update(fileId=id, body={"name": name}, fields="id").execute()
    if folderid:
        # move doc to folder
        service.files().update(fileId=id,
                               addParents=folderid,
                               removeParents=prevParents,
                               fields="id, parents").execute()

    return id


def append_text(docid: str, text: str, service=None):
    if not service:
        service = get_service()
    body = service.files().get_media(fileId=docid).execute()
    print(body)


if __name__ == '__main__':
    copy(template, name="log", folderid="1aaeu256mo8l_oCwf1ZhkPt6zPRqxxBxm")
