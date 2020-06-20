from django.db import models

# Create your models here.


class EduProgram(models.Model):
    name = models.TextField(
        help_text="Name of education program", unique=True
    )
    description = models.TextField(
        help_text="Description of education program"
    )

    def __str__(self):
        return self.name


class ProgramCriteria(models.Model):
    program = models.ForeignKey(EduProgram, on_delete=models.CASCADE)
    label = models.TextField(
        help_text="label of program criteria"
    )
    description = models.TextField(
        help_text="Description of education program"
    )
    value = models.FloatField(
        help_text="Value of education program"
    )
    timestamp = models.DateTimeField(
        help_text="Timestamp of education program"
    )

    def __str__(self):
        return f"{self.program.name}_{self.program}"
