from django.contrib.postgres.fields import ArrayField
# from matrix_field import MatrixFormField
from django.db import models

# Create your models here.
# from matrix_field import MatrixFormField


class Consts(models.Model):
    point = models.CharField(max_length=60, verbose_name='Numer punktu')
    x_coordinate = models.FloatField(verbose_name='Współrzędna X', default=0.000)
    y_coordinate = models.FloatField(verbose_name='Współrzędna Y', default=0.000)
    height = models.FloatField(verbose_name='Wysokość', default=0.000)
    constant = models.BooleanField(default=False, verbose_name='Punkt stały')

class Leveling(models.Model):
    network_name = models.CharField(max_length=60)
    obs_number = models.IntegerField(verbose_name='Numer obserwacji')
    start_point = models.CharField(max_length=60, verbose_name='Numer punktu początkowego')
    end_point = models.CharField(max_length=60, verbose_name='Numer punktu końcowego')
    observation = models.FloatField(verbose_name='Zaobserwowane przewyższenie w [m]')
    accuracy = models.FloatField(verbose_name='Dokładność pomiaru w [m]')

class Student(models.Model):
    name = models.CharField(max_length=60, verbose_name='Imię')
    last_name = models.CharField(max_length=60, verbose_name='Nazwisko')
    index_number = models.IntegerField(verbose_name="Numer indeksu", unique=True)
    RW_set_number = models.IntegerField(verbose_name="Numer zestawu", default=0)
    GW_set_number = models.IntegerField(verbose_name="Numer zestawu", default=0)

    def __str__(self):
        return f'{self.index_number}'

class Statistics(models.Model):
    index_number = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name='Numer indeksu')
    counter = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now=True)

class Points(models.Model):
    point = models.CharField(max_length=60, verbose_name='Numer punktu')
    network_name = models.CharField(max_length=60)
    x_coordinate = models.FloatField(verbose_name='Współrzędna X', default=0.000)
    y_coordinate = models.FloatField( verbose_name='Współrzędna Y', default=0.000)
    height = models.FloatField(verbose_name='Wysokość', default=0.000)


class StudentsResults(models.Model):
    index_number = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name='Numer indeksu')
    date = models.DateTimeField(auto_now_add=True)
    set_num = models.IntegerField(blank=True, null=True)
    data = ArrayField(ArrayField(models.FloatField()),blank=True, null=True)
    HP_matrix = ArrayField(ArrayField(models.FloatField()),blank=True, null=True)
    A_matrix = ArrayField(ArrayField(models.IntegerField()), blank=True, null=True)
    P_matrix = ArrayField(ArrayField(models.FloatField()), blank=True, null=True)
    L_matrix = ArrayField(ArrayField(models.FloatField()), blank=True, null=True)
    ATPA_matrix = ArrayField(ArrayField(models.FloatField()), blank=True, null=True)
    ATPL_matrix = ArrayField(ArrayField(models.FloatField()), blank=True, null=True)
    x_matrix = ArrayField(ArrayField(models.FloatField()),blank=True, null=True)
    V_matrix = ArrayField(ArrayField(models.FloatField()), blank=True, null=True)
    HW_matrix = ArrayField(ArrayField(models.FloatField()), blank=True, null=True)
    dhW_matrix = ArrayField(ArrayField(models.FloatField()), blank=True, null=True)
    mx_matrix = ArrayField(ArrayField(models.FloatField()), blank=True, null=True)
    mV_matrix = ArrayField(ArrayField(models.FloatField()), blank=True, null=True)
    sig_0 = models.FloatField(blank=True, null=True)
    report = ArrayField(ArrayField(models.TextField()), blank=True, null=True)

# class Hirvonen(models.Model):
#         index_number = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name='Numer indeksu')
#         date = models.DateTimeField(auto_now_add=True)
#         XA = models.FloatField(verbose_name='X')
#         YA = models.FloatField(verbose_name='Y')
#         ZA = models.FloatField(verbose_name='Z')

# class Exercise2(models.Model):
#     index_number = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name='Numer indeksu')
#     date = models.DateTimeField(auto_now_add=True)
#     set_num = models.IntegerField(blank=True, null=True)
#     XYZ_A =  ArrayField(ArrayField(models.FloatField()),blank=True, null=True)
#     measurements =  ArrayField(ArrayField(models.FloatField()),blank=True, null=True)
#     lon_lat_H_A =  ArrayField(ArrayField(models.FloatField()),blank=True, null=True)
#     neu_AB =  ArrayField(ArrayField(models.FloatField()),blank=True, null=True)
#     D_matrix =  ArrayField(ArrayField(models.FloatField()),blank=True, null=True)
#     dX_AB = ArrayField(ArrayField(models.FloatField()), blank=True, null=True)
#     XYZ_B = ArrayField(ArrayField(models.FloatField()), blank=True, null=True)
#     lon_lat_H_B =  ArrayField(ArrayField(models.FloatField()),blank=True, null=True)
