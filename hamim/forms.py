from django import forms

class UploadFileForm(forms.Form):
    label_equations = forms.BooleanField(required=False)
    file = forms.FileField()