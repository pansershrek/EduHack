from django.http import HttpResponse
from django.urls import path
from .views import line_chart, line_chart_json


def test_touch(request):
    return HttpResponse("Ok")

urlpatterns = [
    path('', test_touch, name='Test touch'),
    path('chart', line_chart, name='line_chart'),
    path('chartJSON', line_chart_json, name='line_chart_json'),
]
