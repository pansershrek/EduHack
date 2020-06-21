"""
See http://pbpython.com/pandas-google-forms-part1.html for more details
and explanation of how to create the SECRETS_FILE
Purpose of this example is to pull google sheet data into
a pandas DataFrame.
"""
from __future__ import print_function
import gspread
from google.oauth2 import service_account
import pandas as pd
import json
from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload,MediaFileUpload
from googleapiclient.discovery import build
import pprint
import io


SCOPE = ["https://www.googleapis.com/auth/drive"]
SECRETS_FILE = "keys/Hack-f26ccff9907e.json"

def getFormsInformation():
    credentials = service_account.Credentials.from_service_account_file(
            SECRETS_FILE, scopes=SCOPE)

    service = build('drive', 'v3', credentials=credentials)
    results = service.files().list(pageSize=10,
                                   fields="nextPageToken, files(id, name, mimeType)").execute()
    return results


def parse_data_from_google_sheets(file_id, program_id):
    credentials = service_account.Credentials.from_service_account_file(
        SECRETS_FILE, scopes=SCOPE)

    service = build('drive', 'v3', credentials=credentials)
    request = service.files().export_media(fileId=file_id,
                                           mimeType='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    filename = 'Sheet.xlsx'
    fh = io.FileIO(filename, 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
    # print ("Download %d%%." % int(status.progress() * 100))

    df = pd.read_excel('Sheet.xlsx')
    print(df.head(5))


# Get the first sheet
