from django import forms

class CreateNewMod(forms.Form):
    code = forms.CharField(label="Code", max_length = 10)