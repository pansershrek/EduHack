from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.urls import path, reverse
from .views import line_chart, line_chart_json
from django.shortcuts import render

from .models import EduProgram, ProgramCriteria, ParamsWeight

from chartjs.colors import COLORS, next_color
import random
from collections import defaultdict
from .utils.parser_xlsd import parse_teachers_data, parse_university_data, parse_student_data, parse_data_from_google_sheets
import os
from django.shortcuts import redirect
from .utils.dict import translate_criteria, criteria2desc, save_criteria_tags
from .forms import UploadForm, GoogleForm
import io
import pickle
from .utils.google_forms_api import getFormsInformation


import numpy as np
import logging


def label_translate(label):
    return translate_criteria[label] if label in translate_criteria else label


def description_translate(label):
    return criteria2desc[label] if label in criteria2desc else label


def danger_suggest(label):
    return save_criteria_tags[label] if label in save_criteria_tags else ''


def test_touch(request, id):
    return HttpResponse("Ok")


def datetime2str(val):
    return f"{val.month}-{val.year}"


def convert(data_from, data_by):
    for x, y in data_from:
        data_by[str(y)] = x
    kek = list(data_by.items())
    kek.sort(key=lambda x: str(x[0]))
    return [y for (x, y) in kek]


def is_slice(criteria_name):
    return '.' in criteria_name


def compare_charts(request):
    if not request.session.get('to_compare'):
        return render(request, "compare.html")

    timestamps = set()
    graphics_data = []
    for (chart_label, program_id) in request.session['to_compare']:
        if chart_label == "Agg_data":
            graphics_data.append(
                (chart_label, ProgramCriteria.objects.filter(program=program_id)))
        else:
            graphics_data.append((chart_label, ProgramCriteria.objects.filter(
                label=chart_label, program=program_id)))
        timestamps = timestamps.union(
            set([datetime2str(x.timestamp) for x in graphics_data[-1][1]]))
    try:
        coef_sum = sum([x.value for x in ParamsWeight.objects.all()])
    except:
        coef_sum = 1

    if coef_sum <= 0:
        coef_sum = 1
    timestamps = list(timestamps)
    timestamps.sort()
    data_by_date = {x: 0 for x in timestamps}
    return render(request, "compare.html",
                  {
                      "compare": {
                          "data": {
                              "labels": timestamps,
                              "datasets": [
                                  {
                                      "label": label_translate(graphic[0]) + " из " + graphic[1][0].program.name,
                                      "borderColor": f"rgba({166 + random.randint(-100, 40)}, {78 + random.randint(-70, 120)},{46 + random.randint(-30, 100)}, 1)",
                                      'fill': 0, "lineTension":0.1,
                                      "data": convert([(y.value, y.timestamp) for y in graphic[1]], data_by_date.copy()) if graphic[0] != "Agg_data" else
                                      [sum([x.value * get_coef(x) / coef_sum for x in graphic[1]
                                            if datetime2str(x.timestamp) == y]) for y in timestamps]
                                  } for graphic in graphics_data
                              ]
                          }
                      }
                  })


def toggle_to_compare(request):
    try:
        chart_data = [request.GET["chart_label"], request.GET["program_id"]]
    except:
        raise Http404("Неверные парметры запроса")

    if request.session.get('to_compare'):
        if chart_data in request.session['to_compare']:
            request.session['to_compare'].remove(chart_data)
            request.session.modified = True
            return JsonResponse({'action': 'delete'})
    else:
        request.session['to_compare'] = list()
    request.session['to_compare'].append(chart_data)
    request.session.modified = True
    return JsonResponse({'action': 'add'})


def delete_compare_charts(request):
    request.session['to_compare'] = list()
    request.session.modified = True
    return HttpResponseRedirect('/')


def calc_stat_for_chart(chart):
    if len(chart['data']['datasets'][0]['data']) > 1:
        if chart['data']['datasets'][0]['data'][-1] < chart['data']['datasets'][0]['data'][-2]:
            chart['alert'] = True
    chart['stat'] = {}
    arr = np.array(chart['data']['datasets'][0]['data'])
    arr = arr[arr != 0]
    chart['stat']['mean'] = arr.mean()
    chart['stat']['var'] = arr.var()
    chart['stat']['median'] = np.median(arr)


def get_charts_for_slices(request, id=1, slice_type=""):
    crit = ProgramCriteria.objects.get(id=id)
    program_criterias = [criteria for criteria in ProgramCriteria.objects.filter(
        program=crit.program) if is_slice(criteria.label) and crit.label == criteria.label.split('.')[0]]
    if len(program_criterias) > 0:
        criteria_types = defaultdict(list)
        main_criteria = ""
        for criteria in program_criterias:
            criteria_types[criteria.label.split('.')[1]].append(criteria)
            main_criteria = criteria.label.split('.')[0]

        if not slice_type:
            slice_type = list(set(criteria_types.keys()))[0]

        charts = set()
        for criteria in criteria_types[slice_type]:
            charts.add(criteria.label.split('.')[2])

        timestamps = list(set([
            datetime2str(x.timestamp) for x in criteria_types[slice_type]
        ]))
        timestamps.sort()
        data_by_date = {x: 0 for x in timestamps}
        label2id = {
            x: ProgramCriteria.objects.filter(label=main_criteria + "." + slice_type + "." + x)[0].id for x in charts
        }
        if not request.session.get('to_compare'):
            request.session['to_compare'] = list()

        charts = [
            {
                "id": label2id[x],
                "chart_label": main_criteria + "." + slice_type + "." + x,
                "program_id": crit.program.id,
                "is_in_compare": [main_criteria + "." + slice_type + "." + x, str(crit.program.id)] in request.session[
                    'to_compare'],
                "description": description_translate(x),
                "danger_description": danger_suggest(x),
                "data": {
                    "labels": timestamps,
                    "datasets": [
                        {
                            "label": label_translate(x),
                            "borderColor": f"rgba({166 + random.randint(-100, 40)}, {78 + random.randint(-70, 120)},{46 + random.randint(-30, 100)}, 1)",
                            'fill': 0, "lineTension": 0.1,
                            "data": convert([(y.value, y.timestamp) for y in
                                             ProgramCriteria.objects.filter(
                                                 label=main_criteria + "." + slice_type + "." + x,
                                                 program=crit.program)],
                                            data_by_date.copy())
                        }
                    ]
                }
            }
            for x in charts
        ]

        for chart in charts:
            calc_stat_for_chart(chart)

        return render(
            request, "chart_slices.html",
            {
                "criteria": {
                    "name": label_translate(criteria.label.split('.')[0]),
                    "slicename": label_translate(slice_type),
                    "slices": list(criteria_types.keys()),
                    "chartId": id,
                    "charts": charts
                }
            }
        )

    else:
        raise Http404("Для этого графика нет разбивок")


def get_coef(x):
    try:
        lab = x.label
    except:
        return 1

    coef = ParamsWeight.objects.filter(criteria=lab)
    try:
        return coef[0].value
    except:
        return 0


def generateCharts(labels, label2id, criteria_has_slices, program, timestamps, data_by_date, request):
    return [{
        "id": label2id[x],
        "slicesId": label2id[x],
        "has_slices": x in criteria_has_slices,
        "chart_label": x,
        "program_id": program.id,
        "is_in_compare": [x, str(program.id)] in request.session['to_compare'],
        "description": description_translate(x),
        "danger_description": danger_suggest(x),
        "data": {
            "labels": timestamps,
            "datasets": [
                {
                    "label": label_translate(x),
                    "borderColor": f"rgba({166 + random.randint(-100, 40)}, {78 + random.randint(-70, 120)},{46 + random.randint(-30, 100)},1)",
                    'fill': 0, "lineTension": 0.1,
                    "data": convert([(y.value, y.timestamp) for y in
                                     ProgramCriteria.objects.filter(label=x, program=program)],
                                    data_by_date.copy())
                }
            ]
        }
    }
        for x in labels]


def get_charts(request, id=1):
    program = EduProgram.objects.get(id=id)
    program_criterias = ProgramCriteria.objects.filter(program=program)
    criteria_has_slices = set()
    for criteria in program_criterias:
        if is_slice(criteria.label):
            criteria_has_slices.add(criteria.label.split('.')[0])
    try:
        coef_sum = sum([x.value for x in ParamsWeight.objects.all()])
    except:
        coef_sum = 1

    if coef_sum <= 0:
        coef_sum = 1
    program_criterias = list(
        filter(lambda x: not is_slice(x.label), program_criterias))
    timestamps = list(set([
        datetime2str(x.timestamp) for x in program_criterias
    ]))
    timestamps.sort()

    best_labels = {
        "percent_hired_first_year",
        "avg_salary_new/avg_region_sal",
        "student_score",
        "avg_stud_score_per_year",
        "percent_teachers_with_hirsh_noless2",
        "percent_working_student"}
    all_labels = set([x.label for x in program_criterias])
    labels = list(
        all_labels - best_labels
    )
    best_labels = list(best_labels.intersection(all_labels))
    best_labels.sort()
    labels.sort()
    data_by_date = {x: 0 for x in timestamps}
    agg_criteries = {
        "labels": timestamps,
        "datasets": [
            {
                'label': label_translate("Agg_data"),
                "borderColor": f"rgba({166 + random.randint(-100, 40)}, {78 + random.randint(-70, 120)},{46 + random.randint(-30, 100)}, 1)",
                'fill': 0, "lineTension": 0.1,
                "data": [sum([x.value * get_coef(x) / coef_sum for x in program_criterias if datetime2str(x.timestamp) == y]) for y in
                         timestamps]
            }
        ]
    }
    label2id = {
        x: ProgramCriteria.objects.filter(label=x)[0].id for x in labels + best_labels
    }
    if not request.session.get('to_compare'):
        request.session['to_compare'] = list()

    best_charts = generateCharts(
        best_labels, label2id, criteria_has_slices, program, timestamps, data_by_date, request)

    for chart in best_charts:
        calc_stat_for_chart(chart)

    charts = generateCharts(labels, label2id, criteria_has_slices,
                            program, timestamps, data_by_date, request)

    for chart in charts:
        calc_stat_for_chart(chart)

    main_chart = {
        "description": description_translate("Agg_data"),
        "danger_description": danger_suggest("Agg_data"),
        "chart_label": "Agg_data",
        "program_id": program.id,
        "data": agg_criteries,
        "is_in_compare": ["Agg_data", str(program.id)] in request.session['to_compare']
    }

    calc_stat_for_chart(main_chart)

    return render(
        request, "program.html",
        {
            "program": {
                "name": program.name,
                "description": program.description,
                "mainChart": main_chart,
                "bestCharts": best_charts,
                "charts": charts
            }

        }
    )


def get_programms_list(request):
    program = list(EduProgram.objects.all())
    return render(request, "programms_list.html", {"programms": program})


def create_program(request):
    try:
        a = EduProgram.objects.get(name=request.POST['ProgramName'])
        raise Http404("Программа с таким именем уже существует")
    except:
        pass
    program = EduProgram(name=request.POST['ProgramName'], description=request.POST[
                         'ProgramDescription'])
    program.save()
    return HttpResponseRedirect(reverse('program', args=(program.id, )))


def upload_data_students(request):
    if request.method == "POST":
        try:
            form = UploadForm(request.POST, request.FILES)
            if form.is_valid():
                data = io.BytesIO(request.FILES['file'].read())
                parse_student_data(data, request.POST['name'])
                logging.error("Succes save students")
        except BaseException as e:
            logging.error(f"Students {e}")
    else:
        form = UploadForm
        return render(request, "upload_data_students.html", {"form": form})
    return redirect("/")


def upload_data_teachers(request):
    if request.method == "POST":
        try:
            form = UploadForm(request.POST, request.FILES)
            if form.is_valid():
                data = io.BytesIO(request.FILES['file'].read())
                parse_teachers_data(data, request.POST['name'])
                logging.error("Succes save teachers")
        except BaseException as e:
            logging.error(f"Teacher {e}")
    else:
        form = UploadForm
        return render(request, "upload_data_teachers.html", {"form": form})
    return redirect("/")


def upload_data_university(request):
    if request.method == "POST":
        try:
            form = UploadForm(request.POST, request.FILES)
            if form.is_valid():
                data = io.BytesIO(request.FILES['file'].read())
                parse_university_data(data, request.POST['name'])
            logging.error("Succes save University")
        except BaseException as e:
            logging.error(f"University {e}")
    else:
        form = UploadForm
        return render(request, "upload_data_university.html", {"form": form})
    return redirect("/")


def get_google_data(request):
    success = False
    if 'document_id' in request.POST:
        parse_data_from_google_sheets(request.POST['document_id'], request.POST['program_id'])
        success = True
    documents = []
    gfiles = getFormsInformation()
    for gfile in gfiles['files']:
        if gfile['mimeType'].rsplit('.', 1)[1] == 'spreadsheet':
            document = {}
            document['link'] = f"https://docs.google.com/spreadsheets/d/{gfile['id']}"
            document['id'] = gfile['id']
            document['name'] = gfile['name']
            documents.append(document)

    programms = EduProgram.objects.all()
    return render(request, "get_google_data.html",
                  {
                      "success": success,
                      "programs": programms,
                      "documents": documents
                  })

def about_us(request):
    return render(request, "about_us.html")

urlpatterns = [
    path("program/<int:id>", get_charts, name="program"),
    path("chartSlices/<int:id>", get_charts_for_slices, name="chartSlices"),
    path("compareCharts", compare_charts, name="compareCharts"),
    path("deleteCompareCharts", delete_compare_charts, name="deleteCompareCharts"),
    path("toggleToCompare", toggle_to_compare, name="toggleToCompare"),
    path("chartSlices/<int:id>/<str:slice_type>",
         get_charts_for_slices, name="chartSlicesSpec"),
    path("create_program", create_program, name="create_program"),
    path("", get_programms_list, name="programms_list"),
    path("upload_data_university", upload_data_university,
         name="upload_data_university"),
    path("upload_data_teachers", upload_data_teachers,
         name="upload_data_teachers"),
    path("upload_data_students", upload_data_students,
         name="upload_data_students"),
    path("get_google_data", get_google_data, name="get_google_data"),
    path("about_us", about_us, name="about_us")
]
