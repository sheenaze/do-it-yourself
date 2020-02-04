#========  external libraries ==================
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
#========  my files ==================
from .forms import *
from networks.functions_and_classes.external_functions import *
from networks.functions_and_classes.check import *
import urllib.request
from django.utils.encoding import smart_str
from django.contrib.auth.models import User


# ================== Views ===============================================
# class MainStudentView(View):
#     def get(self, request):
#         form = MainViewForm()
#         title = 'Automatyczny sprawdzacz ćwiczeń'
#         return render(request, 'networks/base.html', {'title':title, 'form':form})
#
#
#     def post(self, request):
#         form = MainViewForm(request.POST)
#         title = 'Automatyczny sprawdzacz ćwiczeń'
#         if form.is_valid():
#             index_num = form.cleaned_data['index_number']
#             filename = open()
#             fields = StudentsResults._meta.fields
#             # object = StudentsResults.objects.create(index_number=index_num)
#             student = StudentsResults(index_number=index_num)
#             for i in range(0, len(ranges)):
#                 j = i+3 #field in StudentsResults index
#                 value = readExcercise(filename, ranges[i])
#                 print(i)
#                 setattr(student, fields[j].name, value)
#             student.save()
#             return redirect(f'/results/{index_num}')
#             # return render(request, 'networks/base.html', {'form':form, 'index_num':index_num, 'title':title})
#             # return HttpResponse(student.A_matrix)

class ResultsView(View):
    def get(self, request, index_num):
        student = get_object_or_404(Student, index_number = index_num)
        data_set = student.studentsresults_set.all().order_by('-date')[0]
        # data = data_set.data
        comments = data_set.report

        # context = np.fromstring(data_set.A_matrix)
        context = np.array(data_set.data)
        return render(request, 'networks/results.html', {'comments' : comments})

class MainView(View):
    def get(self, request):
        form = AddUserForm()
        title = 'Sprawdź sobie sam'
        return render(request, 'networks/index.html', {'form':form, 'title':title})
    def post(self, request):
        form = AddUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            name = form.cleaned_data['name']
            last_name = form.cleaned_data['last_name']
            User.objects.create_user(username = username, password= password, name = name, last_name=last_name)
            return redirect('raw_login')
        else:
            return redirect('#contact')
    # def post(self, request):
    #     form = LoginForm(request.POST)
    #     if form.is_valid():
    #         username = form.cleaned_data['login']
    #         password = form.cleaned_data['password']
    #         user = authenticate(username=username, password = password)
    #         print(username, password, user)
    #         if user is not None:
    #             login(request, user)# udało się sprawdzić użytkownika
    #             url = request.GET.get("next") if request.GET.get("next") is not None else 'index'
    #             return redirect(url)
    #         else:
    #             info = 'Błędny login lub hasło'
    #             return render(request, 'networks/index.html', {'form': form, 'info': info}) # nie udało się :(
    #     else:
    #         return HttpResponse('Nie działa')


class RaWView(LoginRequiredMixin, View):
    def get(self, request):
        title = 'Automatyczny sprawdzacz ćwiczeń'
        # form = UploadFileForm()
        # # return HttpResponse(username)
        return render(request, 'networks/RaW.html', {'title': title})

    def post(self, request):
        username = request.user.username
        title = 'Automatyczny sprawdzacz ćwiczeń'

        button = request.POST.get('button')

        if button == 'send_file':
            try:
                index_num = int(username)
                filename = openWindow()
                fields = StudentsResults._meta.fields
                student = Student.objects.get(index_number = index_num)
                student_results = StudentsResults(index_number=student)
                for i in range(0, len(ranges)):
                    j = i + 3  # field in StudentsResults index
                    value = readExcercise(filename, ranges[i])
                    print(i)
                    setattr(student_results, fields[j].name, value)
                student_results.save()
                # comments = checkExcersice(student_results)
                # student_results.report = comments
                # student_results.save()
                return redirect(f'/results/{index_num}')
            except:
                return HttpResponse(self.get(request))

        if button == 'get_data':
            index_num = int(username)
            set_number = Student.objects.get(index_number=index_num).set_number
            data = Leveling.objects.filter(network_name=set_number)

            text = f"Nr obs.,  Pkt. pocz.,    Pkt. końc.,   Obs. [m],  m0 [mm] \n"
            for item in data:
                text += f'{item.obs_number}, {str(item.start_point)}, {item.end_point}, {str(item.observation)}, {str(item.accuracy)} \n'

            filename = f'dane_zestaw_{set_number}.csv'
            response = HttpResponse(text, content_type='text/plain')
            response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
            return response

        if button == 'get_file':
            path = "excel_files/RaW1_Imie_Nazwisko.xlsx"#'./%s_Report.xlsx' % id  # this should live elsewhere, definitely
            filename = 'RaW1_Imie_Nazwisko.xlsx'
            with open(path, "rb") as excel:
                data = excel.read()
            response = HttpResponse(data,
                                    content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = f'attachment; filename= {filename}'
            return response



            # response = HttpResponse(content_type='application/force-download')  # mimetype is replaced by content_type for django 1.7
            # response['Content-Disposition'] = f'attachment; filename={smart_str("RaW1_Imie_Nazwisko.xlsx")}'
            # # response['Content-Disposition'] = 'attachment; filename=%s' % smart_str('RaW1_Imie_Nazwisko.xlsx')
            #
            # response['X-Sendfile'] = smart_str("/home/monika/Projects/MyFinalApp/do-it-yourself/finalApp/excel_files/")
            # # It's usually a good idea to set the 'Content-Length' header too.
            # # You can also set any other required headers: Cache-Control, etc.
            # return response


        if button == 'profile':
            return redirect('/student/')


class StudentView(View):
    def get(self, request):
        username = request.user.username
        student = get_object_or_404(Student, index_number = int(username))

        return render(request, 'networks/student.html', {'student':student})


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'networks/login.html', {'form' : form})
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['login']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password = password)
            print(username, password, user)
            if user is not None:
                login(request, user)# udało się sprawdzić użytkownika
                url = f'/RaW' #request.GET.get("next") if request.GET.get("next") is not None else 'index'
                return redirect(url)
                # return HttpResponse('zalogowany')
            else:
                info = 'Błędny login lub hasło'
                return render(request, 'networks/login.html', {'form': form, 'info': info}) # nie udało się :(
        else:
            return HttpResponse('Nie działa')
            # return render(request, 'exercises/form.html', {'form': form})





