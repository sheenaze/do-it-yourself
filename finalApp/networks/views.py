#========  external libraries ==================
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
import xlrd
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
            object = StudentsResults.objects.create(index_number=index_num)
            # object.index_number = index_num
            # object.save()
            for i in range(0, len(ranges)):
                j = i+3 #field in StudentsResults index
                value = readExcercise(filename, ranges[i])
                setattr(object, fields[j].name, value)
                object.save()

            return render(request, 'networks/base.html', {'form':form, 'file_name':index_num, 'title':title})
            # return HttpResponse(text)

