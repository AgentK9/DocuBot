from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/documents']

DOCUMENT_ID = ""


def get_service():
    """Shows basic usage of the Docs API.
    Prints the title of a sample document.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('creds/doctoken.pickle'):
        with open('creds/doctoken.pickle', 'rb') as token:
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
        with open('creds/doctoken.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('docs', 'v1', credentials=creds)


def append_text(docid: str, text: str, service=None):
    if not service:
        service = get_service()

    endIndex = service.documents().get(documentId=docid, fields="body").execute()["body"]["content"][-1]["endIndex"] - 1
    requests = [
        {
            "insertText": {
                "location": {
                    "index": endIndex
                },
                "text": '\n' + text
            }
        }
    ]
    body = service.documents().batchUpdate(documentId=docid, body={"requests": requests}).execute()


if __name__ == '__main__':
    append_text(DOCUMENT_ID, "test_log")
