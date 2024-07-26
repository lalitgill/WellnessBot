from django import forms
from .models import Reports

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = Reports
        fields = ['file', 'description']