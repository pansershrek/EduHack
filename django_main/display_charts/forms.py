from django import forms
from .models import EduProgram


class UploadForm(forms.Form):
    name = forms.ModelChoiceField(
        queryset=EduProgram.objects.all(), required=True, help_text="Education program name"
    )
    file = forms.FileField(label="File")


class GoogleForm(forms.Form):
    name = forms.CharField(label="Table name")
