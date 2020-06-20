from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import path, reverse
from .views import line_chart, line_chart_json
from django.shortcuts import render

from .models import EduProgram, ProgramCriteria

from chartjs.colors import COLORS, next_color
import random
from collections import defaultdict
from .utils.parser_xlsd import parse_teachers_data, parse_university_data
import os
from django.shortcuts import redirect


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
        return render(
        request, "chart_slices.html",
        {
            "criteria": {
                "name": criteria.label.split('.')[0],
                "slicename": slice_type,
                "slices": list(criteria_types.keys()),
                "chartId": id,
                "charts": [
                    {
                        "id": label2id[x],
                        "data": {
                            "labels": timestamps,
                            "datasets": [
                                {
                                    "label": x,
                                    "backgroundColor": f"rgba({166 + random.randint(-100, 40)}, {78 + random.randint(-70, 120)},{46 + random.randint(-30, 100)}, 0.5)",
                                    "data": convert([(y.value, y.timestamp) for y in
                                                     ProgramCriteria.objects.filter(label=main_criteria+"."+slice_type+"."+x, program=crit.program)],
                                                    data_by_date.copy())
                                }
                            ]
                        }
                    }
                    for x in charts
                ]
            }
        }
    )

    else:
        raise Http404("Для этого графика нет разбивок")


def get_charts(request, id=1):
    program = EduProgram.objects.get(id=id)
    program_criterias = ProgramCriteria.objects.filter(program=program)
    criteria_has_slices = set()
    for criteria in program_criterias:
        if is_slice(criteria.label):
            criteria_has_slices.add(criteria.label.split('.')[0])

    program_criterias = list(
        filter(lambda x: not is_slice(x.label), program_criterias))
    timestamps = list(set([
        datetime2str(x.timestamp) for x in program_criterias
    ]))
    timestamps.sort()
    labels = list(
        set([x.label for x in program_criterias])
    )
    labels.sort()
    data_by_date = {x: 0 for x in timestamps}
    agg_criteries = {
        "labels": timestamps,
        "datasets": [
            {
                "label": "Agg data",
                "backgroundColor": f"rgba({166 + random.randint(-100, 40)}, {78 + random.randint(-70, 120)},{46 + random.randint(-30, 100)}, 0.5)",
                "data": [sum([x.value for x in program_criterias if datetime2str(x.timestamp) == y]) for y in
                         timestamps]
            }
        ]
    }
    label2id = {
        x: ProgramCriteria.objects.filter(label=x)[0].id for x in labels
    }
    return render(
        request, "program.html",
        {
            "program": {
                "name": program.name,
                "description": program.description,
                "mainChart": {
                    "data": agg_criteries
                },
                "charts": [
                    {
                        "id": label2id[x],
                        "slicesId": label2id[x],
                        "has_slices": x in criteria_has_slices,
                        "data": {
                            "labels": timestamps,
                            "datasets": [
                                {
                                    "label": x,
                                    "backgroundColor": f"rgba({166 + random.randint(-100, 40)}, {78 + random.randint(-70, 120)},{46 + random.randint(-30, 100)}, 0.5)",
                                    "data": convert([(y.value, y.timestamp) for y in
                                                     ProgramCriteria.objects.filter(label=x, program=program)],
                                                    data_by_date.copy())
                                }
                            ]
                        }
                    }
                    for x in labels
                ]
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


def upload_data(request, id_prog, file_path):
    #ex_file = "display_charts/utils/testXsld/Univer_Info_Data.xlsx"
    file_path = os.path.join("display_charts/utils/testXsld/", file_path)
    obj = open(file_path, 'rb')
    parse_university_data(obj, id_prog)
    return redirect("/")


urlpatterns = [
    path("program/<int:id>", get_charts, name="program"),
    path("chartSlices/<int:id>", get_charts_for_slices, name="chartSlices"),
    path("chartSlices/<int:id>/<str:slice_type>",
         get_charts_for_slices, name="chartSlicesSpec"),
    path("create_program", create_program, name="create_program"),
    path("", get_programms_list, name="programms_list"),
    path("upload_data/<int:id_prog>/<str:file_path>",
         upload_data, name="upload_data"),
]
