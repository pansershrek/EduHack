from django.http import HttpResponse
from django.urls import path
from .views import line_chart, line_chart_json
from django.shortcuts import render

from .models import EduProgram, ProgramCriteria

from chartjs.colors import COLORS, next_color
import random


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
    program_criterias = [criteria for criteria in ProgramCriteria.objects.filter(program=program) if not is_slice(criteria.label)]

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
        request, "charts.html",
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


urlpatterns = [
    path("charts/<int:id>", get_charts, name="charts"),
    path("charts/", get_charts, name="charts"),
    path("chartSlices/<int:id>", test_touch, name="chartSlices")
]
