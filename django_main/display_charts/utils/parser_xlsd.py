import pandas as pd
import xlrd
import numpy as np
from display_charts.models import ProgramCriteria, EduProgram
from django.utils import timezone
from datetime import datetime
import traceback
from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload,MediaFileUpload
from googleapiclient.discovery import build
import pprint
import io
import itertools

SCOPE = ["https://www.googleapis.com/auth/drive"]
SECRETS_FILE = "keys/Hack-f26ccff9907e.json"

def load2db(col, val, date, pr_id):
    tmp = ProgramCriteria(label=col, description="Paste From Map",
                          value=val, timestamp=date, program=pr_id)
    tmp.save()


def parse_data_from_google_sheets(file_id, program_id):
    credentials = service_account.Credentials.from_service_account_file(
        SECRETS_FILE, scopes=SCOPE)

    service = build('drive', 'v3', credentials=credentials, cache_discovery=False)
    request = service.files().export_media(fileId=file_id,
                                           mimeType='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
    # print ("Download %d%%." % int(status.progress() * 100))
    parse_university_data(fh, program_id)


def parse_university_data(excel_file, program_id):
    try:
        program_id = EduProgram.objects.get(id=program_id)
    except:
        return
    data = pd.read_excel(excel_file)
    data.columns = itertools.chain(["date"], data.columns[1:])
    year_arr = data.get("date").array

    for col in data.columns[1:]:
        arr = data.get(col).array.fillna(0)
        for i in range(len(year_arr)):
            temp_date = year_arr[i].date()
            load2db(col, arr[i], temp_date, program_id)


def parse_student_data(excel_data, program_id):
    try:
        program_id = EduProgram.objects.get(id=program_id)
    except:
        return
    data = pd.read_excel(excel_data)
    year_arr = data.get("date").array
    id_stud = data.get("id_student").array
    cnt_subj = data.get("cnt_subjects").array.fillna(0)
    n = len(data.columns)
    i = 1
    cnt_stud = len(set(id_stud))
    for i in range(len(year_arr)):
        temp_date = year_arr[i].date()
        sum = 0
        for col in data.columns[3:]:
            sum += data.get(col).array.fillna(0)[i]
        sum /= (n - 3)
        load2db("avg_stud_score_per_year.avg_semester_student." +
                str(id_stud[i]), sum, temp_date, program_id)

    new_data = data.groupby(['date']).sum()

    year_arr_2 = list(set(year_arr))
    for i in range(len(year_arr_2)):
        temp_date = year_arr[i].date()
        cnt = new_data.get("cnt_subjects")[i]
        for col in new_data.columns[2:]:
            load2db("avg_stud_score_per_year.avg_semester_subject." +
                    col[-1:], new_data.get(col)[i] / cnt, temp_date, program_id)


def parse_teachers_data(excel_file, program_id):
    try:
        program_id = EduProgram.objects.get(id=program_id)
    except:
        return
    data = pd.read_excel(excel_file)
    year_arr = data.get("date").array
    p2p_arr = data.get("p2p_score").array
    stud_arr = data.get("student_score").array
    teachers_id = data.get("teacher_id").array
    number_of_art = data.get("number_of_articles").array

    for i in range(len(year_arr)):
        temp_date = year_arr[i].date()
        tmp = ProgramCriteria(label="p2p_score", description="Peer-2-Peer Score from other Teachers(AVG)",
                              value=p2p_arr[i], timestamp=temp_date, program=program_id)
        tmp.save()
        tmp = ProgramCriteria(label="student_score", description="Teacher's Scores from students(AVG)",
                              value=stud_arr[i], timestamp=temp_date, program=program_id)
        tmp.save()
        tmp = ProgramCriteria(label="number_of_articles.teachers." + str(teachers_id[i]), description="Count of written articles by Teacher " + str(teachers_id[
                              i]), value=number_of_art[i], timestamp=temp_date, program=program_id)
        tmp.save()
