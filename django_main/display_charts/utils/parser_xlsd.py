import pandas as pd
import xlrd
import numpy as np
from display_charts.models import ProgramCriteria, EduProgram
from django.utils import timezone
from datetime import datetime
import traceback


def load2db(col, val, date, pr_id):
    tmp = ProgramCriteria(label=col, description="Paste From Map",
                          value=val, timestamp=date, program=pr_id)
    tmp.save()


def parse_university_data(excel_file, program_id):
    try:
        program_id = EduProgram.objects.get(id=program_id)
    except:
        return
    data = pd.read_excel(excel_file)
    year_arr = data.get("date").array

    for col in data.columns[1:]:
        arr = data.get(col).array.fillna(0)
        for i in range(len(year_arr)):
            temp_date = year_arr[i].date()
            load2db(col, arr[i], temp_date, program_id)


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
