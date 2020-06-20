from django.http import HttpResponse
from django.urls import path
from .views import line_chart, line_chart_json
from django.shortcuts import render


def test_touch(request):
    return HttpResponse("Ok")


class kek_1:
    id = 1
    name = "lel"


def kek(request):
    return render(request, "programms_list.html", {"programms": [{"id": "1", "name": "kek"}, ]})


urlpatterns = [
    path('', test_touch, name='Test touch'),
    path('chart', line_chart, name='line_chart'),
    path('chartJSON', line_chart_json, name='line_chart_json'),
    path('kek', kek, name="kek"),
    path('programm/<int:id>', test_touch, name="programm")
]
