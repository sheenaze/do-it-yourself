from django.http import HttpRequest
from django.shortcuts import render
from tkinter import *
from tkinter import filedialog

from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView


from .models import  *
from .forms import *
from .functions import *

import xlrd
# class MainView(CreateView):
#     model = Statistics
#     fields = ['index_number', 'set_number']
#     success_url = reverse_lazy("")




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
            obj = Statistics.objects.filter(index_number = index_num)
            if len(obj) == 0:
                counter = 1
            else:
                counter = len(obj)+1
            filename = open()
            Statistics.objects.create(counter= counter, index_number=index_num)
            xls_file = xlrd.open_workbook(filename)
            sheet = xls_file.sheet_by_index(0)
            print(sheet.cell_value(23, 0))
            return render(request, 'networks/base.html', {'form':form, 'file_name':index_num, 'title':title})

