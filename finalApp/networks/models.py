from django.contrib.postgres.fields import ArrayField
from django.db import models
# Create your models here.

class Points(models.Model):
    point = models.CharField(max_length=60, verbose_name='Numer punktu')
    x_coordinate = models.DecimalField(max_digits=11, decimal_places=4, verbose_name='Współrzędna X', default=0.000)
    y_coordinate = models.DecimalField(max_digits=11, decimal_places=4, verbose_name='Współrzędna Y', default=0.000)
    height = models.DecimalField(max_digits=8, decimal_places=4, verbose_name='Wysokość', default=0.000)
    constant = models.BooleanField(default=False, verbose_name='Punkt stały')

class Leveling(models.Model):
    network_name = models.CharField(max_length=60)
    obs_number = models.IntegerField(verbose_name='Numer obserwacji')
    start_point = models.CharField(max_length=60, verbose_name='Numer punktu początkowego')
    end_point = models.CharField(max_length=60, verbose_name='Numer punktu końcowego')
    observation = models.DecimalField(max_digits=8, decimal_places=4, verbose_name='Zaobserwowane przewyższenie w [m]')
    accuracy = models.DecimalField(max_digits=4, decimal_places=3, verbose_name='Dokładność pomiaru w [m]')

class Student(models.Model):
    name = models.CharField(max_length=60, verbose_name='Imię')
    last_name = models.CharField(max_length=60, verbose_name='Nazwisko')
    index_number = models.IntegerField(verbose_name="Numer indeksu", unique=True)
    set_number = models.IntegerField(verbose_name="Numer zestawu")

    def __str__(self):
        return f'{self.index_number}'

class Statistics(models.Model):
    index_number = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name='Numer indeksu')
    counter = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now=True)

class StudentsResults(models.Model):
    index_number = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name='Numer indeksu')
    date = models.DateTimeField(auto_now_add=True)
    set = models.IntegerField()
    data = ArrayField(ArrayField(models.DecimalField(max_digits=8, decimal_places=4)))
    A_matrix = ArrayField(ArrayField(models.IntegerField()))




# ranges = [
#     'C2:C2', #set number
#     'B6:D19', #raw data
#     'A23:G36', #A
#     'A39:N52', #LP
#     'H23:H36'# L
#     'A57:G63', #ATPA
#     'H57:H63', #ATPL
#     'C69:C75', #x
#     'G69:G82', #V
#     'D69:D75', #HW
#     'H69:H82', #ObsW
#     'C88:C88', #sig_0
#     'F90:F96', #mx
#     'G90:G103' #mv
# ]
