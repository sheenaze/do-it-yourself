from django.contrib.postgres.fields import ArrayField
# from matrix_field import MatrixFormField
from django.db import models

# Create your models here.
# from matrix_field import MatrixFormField

class Consts(models.Model):
    point = models.CharField(max_length=60, verbose_name='Numer punktu')
    x_coordinate = models.FloatField(verbose_name='Współrzędna X', default=0.000)
    y_coordinate = models.FloatField(verbose_name='Współrzędna Y', default=0.000)
    height = models.DecimalField(max_digits=8, decimal_places=4, verbose_name='Wysokość', default=0.000)
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
    set_number = models.IntegerField(verbose_name="Numer zestawu")

    def __str__(self):
        return f'{self.index_number}'

class Statistics(models.Model):
    index_number = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name='Numer indeksu')
    counter = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now=True)

# class StudentsResults(models.Model):
#     index_number = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name='Numer indeksu')
#     date = models.DateTimeField(auto_now_add=True)
#     set = models.IntegerField(blank=True, null=True)
#     data = models.TextField(blank=True, null=True)
#     A_matrix = models.TextField(blank=True, null=True)
#     P_matrix =  models.TextField(blank=True, null=True)
#     L_matrix =  models.TextField(blank=True, null=True)
#     ATPA_matrix =  models.TextField(blank=True, null=True)
#     ATPL_matrix =  models.TextField(blank=True, null=True)
#     x_matrix =  models.TextField(blank=True, null=True)
#     V_matrix = models.TextField(blank=True, null=True)
#     HW_matrix = models.TextField(blank=True, null=True)
#     dhW_matrix =  models.TextField(blank=True, null=True)
#     mx_matrix =  models.TextField(blank=True, null=True)
#     mV_matrix =  models.TextField(blank=True, null=True)
#     sig_0 =  models.TextField(blank=True, null=True)

class Points(models.Model):
    network_name = models.ForeignKey(Leveling, on_delete=models.CASCADE)
    x_coordinate = models.FloatField(verbose_name='Współrzędna X', default=0.000)
    y_coordinate = models.FloatField( verbose_name='Współrzędna Y', default=0.000)
    height = models.FloatField(verbose_name='Wysokość', default=0.000)


    # def setField(self, field_num,value):
    #     field = self._meta.fields[field_num].name
    #     self.field = value
    # def get_fields(self, value):
    #     return [(field.name, field.value_to_string(value)) for field in StudentsResults._meta.fields]




# class StudentsResults(models.Model):
#     index_number = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name='Numer indeksu')
#     date = models.DateTimeField(auto_now_add=True)
#     set = models.IntegerField(blank=True, null=True)
#     data =ArrayField(models.FloatField(blank=True, null=True))
#     A_matrix = ArrayField(models.IntegerField(blank=True, null=True))
#     P_matrix = ArrayField(models.FloatField(blank=True, null=True))
#     L_matrix = ArrayField(models.FloatField(blank=True, null=True))
#     ATPA_matrix = ArrayField(models.FloatField(blank=True, null=True))
#     ATPL_matrix = ArrayField(models.FloatField(blank=True, null=True))
#     x_matrix =ArrayField(models.FloatField(blank=True, null=True))
#     V_matrix = ArrayField(models.FloatField(blank=True, null=True))
#     HW_matrix =ArrayField(models.FloatField(blank=True, null=True))
#     dhW_matrix = ArrayField(models.FloatField(blank=True, null=True))
#     mx_matrix = ArrayField(models.FloatField(blank=True, null=True))
#     mV_matrix = ArrayField(models.FloatField(blank=True, null=True))
#     sig_0 = models.FloatField(blank=True, null=True)


# #
class StudentsResults(models.Model):
    index_number = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name='Numer indeksu')
    date = models.DateTimeField(auto_now_add=True)
    set = models.IntegerField(blank=True, null=True)
    data = ArrayField(ArrayField(models.FloatField(blank=True, null=True)))
    A_matrix = ArrayField(ArrayField(models.IntegerField(blank=True, null=True)))
    P_matrix = ArrayField(ArrayField(models.FloatField(blank=True, null=True)))
    L_matrix = ArrayField(ArrayField(models.FloatField(blank=True, null=True)))
    ATPA_matrix = ArrayField(ArrayField(models.FloatField(blank=True, null=True)))
    ATPL_matrix = ArrayField(ArrayField(models.FloatField(blank=True, null=True)))
    x_matrix = ArrayField(ArrayField(models.FloatField(blank=True, null=True)))
    V_matrix = ArrayField(ArrayField(models.FloatField(blank=True, null=True)))
    HW_matrix = ArrayField(ArrayField(models.FloatField(blank=True, null=True)))
    dhW_matrix = ArrayField(ArrayField(models.FloatField(blank=True, null=True)))
    mx_matrix = ArrayField(ArrayField(models.FloatField(blank=True, null=True)))
    mV_matrix = ArrayField(ArrayField(models.FloatField(blank=True, null=True)))
    sig_0 = models.FloatField(blank=True, null=True)






# ranges = [
#     'C2:C2', #set number
#     'B6:D19', #raw data
#     'A23:G36', #A
#     'A39:N52', #P
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
