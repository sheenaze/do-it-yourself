from django import forms
from django.forms import ModelForm
from .models import *


class MainViewForm(ModelForm):
    class Meta:
        model = StudentsResults
        fields = ['index_number']

class LoginForm(forms.Form):
    login = forms.CharField(label = 'Login', max_length=120)
    password = forms.CharField(label='Password', max_length=120, widget=forms.PasswordInput)
    # submit = forms.CharField()

class UploadFileForm(forms.Form):
    # title = forms.CharField(max_length=50)
    file = forms.FileField()
