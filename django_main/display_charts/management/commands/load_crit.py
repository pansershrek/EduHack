from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models import Q

from display_charts.utils.dict.dict import translate_criteria
from display_charts.models import ParamsWeight


class Command(BaseCommand):
    help = "Load crits"

    def handle(self, *args, **options):
        for key in translate_criteria:
            par = ParamsWeight(criteria=key, value=1)
            par.save()
