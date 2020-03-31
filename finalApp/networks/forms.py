from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import *
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe


class MainViewForm(ModelForm):
    class Meta:
        model = StudentsResults
        fields = ['index_number']


class LoginForm(forms.Form):
    login = forms.CharField(label='Login', max_length=120)
    password = forms.CharField(label='Hasło', max_length=120, widget=forms.PasswordInput)
    # submit = forms.CharField()


class UploadFileForm(forms.Form):
    # title = forms.CharField(max_length=50)
    file = forms.FileField()


class AddUserForm(forms.Form):
    username = forms.IntegerField(label='Numer indeksu')
    password = forms.CharField(label='Hasło', max_length=120, widget=forms.PasswordInput)
    rep_password = forms.CharField(label='Powtórz hasło', max_length=120, widget=forms.PasswordInput)

    # name =  forms.CharField(label = 'Imię', max_length=120)
    # last_name =  forms.CharField(label = 'Nazwisko', max_length=120)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")

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


class HirvonenForm(forms.Form):
    XA = forms.FloatField(label='X_A')
    YA = forms.FloatField(label='Y_A')
    ZA = forms.FloatField(label='Z_A')
    FiA_D = forms.IntegerField(label='Fi', min_value=-90, max_value=90)
    FiA_M = forms.IntegerField(min_value=0, max_value=59)
    FiA_S = forms.FloatField(min_value=0, max_value=59.99999)
    LbdA_D = forms.IntegerField(label='Lbd', min_value=0, max_value=360)
    LbdA_M = forms.IntegerField(min_value=0, max_value=59)
    LbdA_S = forms.FloatField(min_value=0, max_value=59.99999)
    HA = forms.FloatField(label='H_A')


class NeuXYZ_Form(forms.Form):
    north = forms.FloatField(label='n')
    east = forms.FloatField(label='e')
    up = forms.FloatField(label='u')
    dX = forms.FloatField(label='dX')
    dY = forms.FloatField(label='dY')
    dZ = forms.FloatField(label='dZ')
    FiA_D = forms.IntegerField(label='Fi', min_value=-90, max_value=90)
    FiA_M = forms.IntegerField(min_value=0, max_value=59)
    FiA_S = forms.FloatField(min_value=0, max_value=59.99999)
    LbdA_D = forms.IntegerField(label='Lbd', min_value=0, max_value=360)
    LbdA_M = forms.IntegerField(min_value=0, max_value=59)
    LbdA_S = forms.FloatField(min_value=0, max_value=59.99999)


class KiviojVincentyForm(forms.Form):
    FiA_D = forms.IntegerField(label='Fi', min_value=-90, max_value=90)
    FiA_M = forms.IntegerField(min_value=0, max_value=59)
    FiA_S = forms.FloatField(min_value=0, max_value=59.99999)

    ds_number = forms.IntegerField(label='liczba odcinków', min_value= 1, max_value= 9999999999)
    LbdA_D = forms.IntegerField(label='Lbd', min_value=0, max_value=360)
    LbdA_M = forms.IntegerField(min_value=0, max_value=59)
    LbdA_S = forms.FloatField(min_value=0, max_value=59.99999)

    distance = forms.FloatField(label='s')
    AzAB_D = forms.IntegerField(label='Lbd', min_value=0, max_value=360)
    AzAB_M = forms.IntegerField(min_value=0, max_value=59)
    AzAB_S = forms.FloatField(min_value=0, max_value=59.99999)

    FiB_D = forms.IntegerField(label='Fi', min_value=-90, max_value=90)
    FiB_M = forms.IntegerField(min_value=0, max_value=59)
    FiB_S = forms.FloatField(min_value=0, max_value=59.99999)

    LbdB_D = forms.IntegerField(label='Lbd', min_value=0, max_value=360)
    LbdB_M = forms.IntegerField(min_value=0, max_value=59)
    LbdB_S = forms.FloatField(min_value=0, max_value=59.99999)

    AzBA_D = forms.IntegerField(label='Lbd', min_value=0, max_value=360)
    AzBA_M = forms.IntegerField(min_value=0, max_value=59)
    AzBA_S = forms.FloatField(min_value=0, max_value=59.99999)

# class Exercise_2Form(forms.Form):
#     XA = forms.FloatField(label = 'X_A')
#     YA = forms.FloatField(label = 'Y_A')
#     ZA = forms.FloatField(label = 'Z_A')
#     zenith = forms.IntegerField(label = 'z_{AB}')
#     azimuth = forms.IntegerField(label = 'Az_{AB}')
#     distance = forms.IntegerField(label = 's_{AB}')
#     FiA_D = forms.IntegerField(label='Fi', min_value=-90, max_value=90)
#     FiA_M = forms.IntegerField(min_value=0, max_value=59)
#     FiA_S = forms.FloatField(min_value=0, max_value=59.99999)
#
#     LbdA_D = forms.IntegerField(label='Fi', min_value=-90, max_value=90)
#     LbdA_M = forms.IntegerField(min_value=0, max_value=59)
#     LbdA_S = forms.FloatField(min_value=0, max_value=59.99999)
#     HA = forms.FloatField(label='H_A')
#
#
#     neu_n = forms.FloatField(label='n')
#     neu_e = forms.FloatField(label='e')
#     neu_u = forms.FloatField(label='u')
#
#
#     D11 = forms.FloatField()
#     D12 = forms.FloatField()
#     D13 = forms.FloatField()
#     D21 = forms.FloatField()
#     D22 = forms.FloatField()
#     D23 = forms.FloatField()
#     D31 = forms.FloatField()
#     D32 = forms.FloatField()
#     D33 = forms.FloatField()
#
#     dX_AB = forms.FloatField(label='dX_AB')
#     dY_AB = forms.FloatField(label='dY_AB')
#     dZ_AB = forms.FloatField(label='dZ_AB')
#
#     XB = forms.FloatField(label = 'X_B')
#     YB = forms.FloatField(label = 'Y_B')
#     ZB = forms.FloatField(label = 'Z_B')
#
#     FiB_D = forms.IntegerField(label='Fi', min_value=-90, max_value=90)
#     FiB_M = forms.IntegerField(min_value=0, max_value=59)
#     FiB_S = forms.FloatField(min_value=0, max_value=59.99999)
#
#     LbdB_D = forms.IntegerField(label='Fi', min_value=-90, max_value=90)
#     LbdB_M = forms.IntegerField(min_value=0, max_value=59)
#     LbdB_S = forms.FloatField(min_value=0, max_value=59.99999)
#     HB = forms.FloatField(label='H_A')
#
# class Exercise_3Form(forms.Form):
#     pass
#
# class Exercise_4Form(forms.Form):
#     pass
#
# class Exercise_5Form(forms.Form):
#     pass
#
# class Exercise_6Form(forms.Form):
#     pass
