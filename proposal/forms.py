from django import forms
from .models import Document

# class UploadFileForm(forms.Form):
#     file = forms.FileField()

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields =('title','uploaded_file')