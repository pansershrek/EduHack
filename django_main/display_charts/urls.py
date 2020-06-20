from django.http import HttpResponse
from django.urls import path
from .views import line_chart, line_chart_json
from django.shortcuts import render


def test_touch(request, id):
    return HttpResponse("Ok")


class kek_1:
    id = 1
    name = "lel"


def kek(request):
    return render(request, "programms_list.html", {"programms": [{"id": "1", "name": "kek"}, ]})


def lel(request):
    return render(
        request, "chart_slices.html",
        {
            "criteria": {
                "name": "NAME", "slicename": "SLICENAME",
                "slices": [
                    {"id": "1", "name": "name1"},
                    {"id": "2", "name": "name2"}
                ],
                "charts": [
                    {"id": 1, "data": [[1, 2, 3], [1, 2, 3]]},
                    {"id": 2, "data": [[1, 2, 3], [1, 2, 3]]}
                ]
            },

        }
    )

urlpatterns = [
    path('', test_touch, name='Test touch'),
    path('chart', line_chart, name='line_chart'),
    path('chartJSON', line_chart_json, name='line_chart_json'),
    path('kek', kek, name="kek"),
    path('lel', lel, name="lel"),
    path('programm/<int:id>', test_touch, name="programm"),
    path('slice/<int:id>', test_touch, name="slice")
]
