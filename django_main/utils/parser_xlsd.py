import pandas as pd
import xlrd
import numpy as np
from django_main.display_charts.models import ProgramCriteria
from django.utils import timezone
from datetime import datetime

def parse_teachers_data(excel_file, program_id):
    data = pd.read_excel(excel_file)
    year_arr = data.get("date").array
    p2p_arr = data.get("p2p_score").array
    stud_arr = data.get("student_score").array
    teachers_id = data.get("teachers_id").array
    number_of_art = data.get("number_of_articles").array

    for i in range(len(year_arr)):
        temp_date = datetime.strptime(year_arr[i], "%m-%Y").date()
        tmp = ProgramCriteria(label="p2p_score", description="Peer-2-Peer Score from other Teachers(AVG)", value=p2p_arr[i], timestamp=temp_date, program=program_id)
        tmp.save()
        tmp = ProgramCriteria(label="student_score", description="Teacher's Scores from students(AVG)",
                              value=stud_arr[i], timestamp=temp_date, program=program_id)
        tmp.save()
        tmp = ProgramCriteria(label="number_of_articles.teachers." + teachers_id[i], description="Count of written articles by Teacher " + teachers_id[i], value=number_of_art[i], timestamp=temp_date, program=program_id)
        tmp.save()



#ex_file = "testXsld/Teacher_Data.xlsx"

#obj = open(ex_file,'rb')