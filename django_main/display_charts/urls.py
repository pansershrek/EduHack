from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import path, reverse
from .views import line_chart, line_chart_json
from django.shortcuts import render

from .models import EduProgram, ProgramCriteria

from chartjs.colors import COLORS, next_color
import random

from .utils.parser_xlsd import parse_teachers_data


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


def get_charts(request, id=1):
    program = EduProgram.objects.get(id=id)
    program_criterias = [criteria for criteria in ProgramCriteria.objects.filter(
        program=program) if not is_slice(criteria.label)]

    timestamps = [
        datetime2str(x.timestamp) for x in program_criterias
    ]
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
    program = EduProgram(name=request.POST['ProgramName'], description=request.POST['ProgramDescription'])
    program.save()
    return HttpResponseRedirect(reverse('program', args=(program.id, )))


def kek(request):
    ex_file = "display_charts/utils/testXsld/Teacher_Data.xlsx"
    obj = open(ex_file, 'rb')
    parse_teachers_data(obj, 1)


urlpatterns = [
    path("program/<int:id>", get_charts, name="program"),
    path("charts/", get_charts, name="charts"),
    path("chartSlices/<int:id>", test_touch, name="chartSlices"),
    path("/create_program", create_program, name="create_program"),
    path("", get_programms_list, name="programms_list")
]
