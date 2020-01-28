from django import forms
from django.forms import ModelForm
from .models import *


class MainViewForm(ModelForm):
    class Meta:
        model = StudentsResults
        fields = ['index_number']
