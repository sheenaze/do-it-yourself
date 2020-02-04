from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import *
from django.core.exceptions import ValidationError

class MainViewForm(ModelForm):
    class Meta:
        model = StudentsResults
        fields = ['index_number']

class LoginForm(forms.Form):
    login = forms.CharField(label = 'Login', max_length=120)
    password = forms.CharField(label='Hasło', max_length=120, widget=forms.PasswordInput)
    # submit = forms.CharField()

class UploadFileForm(forms.Form):
    # title = forms.CharField(max_length=50)
    file = forms.FileField()

class AddUserForm(forms.Form):
    username = forms.IntegerField(label = 'Numer indeksu')
    password = forms.CharField(label='Hasło', max_length=120, widget=forms.PasswordInput)
    rep_password = forms.CharField(label='Confirmed Password', max_length=120, widget=forms.PasswordInput)
    name =  forms.CharField(label = 'Imię', max_length=120)
    last_name =  forms.CharField(label = 'Nazwisko', max_length=120)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("login")

        userV1 = Student.objects.filter(index_number=username)
        if len(userV1) == 0:
            raise ValidationError('Student o podanym numerze indeksu nie figuruje na liście obecności')

        userV2 = User.objects.filter(username=username)
        if len(userV2) != 0:
            raise ValidationError('Na podany numer indeksu dokonano już rejestracji')

        password = cleaned_data.get('password')
        rep_password = cleaned_data.get('rep_password')
        if password != rep_password:
            raise forms.ValidationError('Hasło i powtórzone hasło się nie zgadzają')

class ResetPasswordForm(forms.Form):
    password = forms.CharField(label='Wprowadź nowe hasło', max_length=120, widget=forms.PasswordInput)
    rep_password = forms.CharField(label='Powtórz hasło', max_length=120, widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        rep_password = cleaned_data.get('rep_password')
        if password != rep_password:
            raise forms.ValidationError('Hasło i powtórzone hasło się nie zgadzają')