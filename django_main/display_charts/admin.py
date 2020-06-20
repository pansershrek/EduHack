from django.contrib import admin
from .models import EduProgram, ProgramCriteria, ParamsWeight

# Register your models here.


@admin.register(EduProgram)
class EduProgramAdmin(admin.ModelAdmin):
    pass


@admin.register(ProgramCriteria)
class ProgramCriteriaAdmin(admin.ModelAdmin):
    pass


@admin.register(ParamsWeight)
class ParamsWeightAdmin(admin.ModelAdmin):
    pass
