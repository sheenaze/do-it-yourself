#========  external libraries ==================
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
import xlrd
import numpy as np
#========  my files ==================
from .models import  *
from .forms import *
from .external_functions import *


# ================== Views ===============================================
class MainView(View):
    def get(self, request):
        form = MainViewForm()
        title = 'Automatyczny sprawdzacz ćwiczeń'
        return render(request, 'networks/base.html', {'title':title, 'form':form})


    def post(self, request):
        form = MainViewForm(request.POST)
        title = 'Automatyczny sprawdzacz ćwiczeń'
        if form.is_valid():
            index_num = form.cleaned_data['index_number']
            filename = open()
            fields = StudentsResults._meta.fields
            # object = StudentsResults.objects.create(index_number=index_num)
            student = StudentsResults(index_number=index_num)
            for i in range(0, len(ranges)):
                j = i+3 #field in StudentsResults index
                value = readExcercise(filename, ranges[i])
                print(i)
                setattr(student, fields[j].name, value)
            student.save()
            return redirect(f'/results/{index_num}')
            # return render(request, 'networks/base.html', {'form':form, 'index_num':index_num, 'title':title})
            # return HttpResponse(student.A_matrix)

class ResultsView(View):
    def get(self, request, index_num):
        student = get_object_or_404(Student, index_number = index_num)
        data_set = student.studentsresults_set.all().order_by('-date')[0]
        # context = np.fromstring(data_set.A_matrix)
        context = np.array(data_set.A_matrix)
        return render(request, 'networks/results.html', {'context' : context})

