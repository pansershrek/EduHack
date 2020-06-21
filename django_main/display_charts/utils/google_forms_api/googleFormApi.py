"""
See http://pbpython.com/pandas-google-forms-part1.html for more details
and explanation of how to create the SECRETS_FILE
Purpose of this example is to pull google sheet data into
a pandas DataFrame.
"""
from google.oauth2 import service_account
import pandas as pd
import json
from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload,MediaFileUpload
from googleapiclient.discovery import build
import io


SCOPE = ["https://www.googleapis.com/auth/drive"]
SECRETS_FILE = "keys/Hack-f26ccff9907e.json"

def getFormsInformation():
    credentials = service_account.Credentials.from_service_account_file(
            SECRETS_FILE, scopes=SCOPE)

    service = build('drive', 'v3', credentials=credentials, cache_discovery=False)
    results = service.files().list(pageSize=10,
                                   fields="nextPageToken, files(id, name, mimeType)").execute()
    return results




# Get the first sheet
