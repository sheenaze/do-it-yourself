#========  external libraries ==================
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from networks.functions_and_classes.check import *

#========  my files ==================
from .forms import *
# from geodesy.algorithms import *
from networks.geodesy.geodesy_exercises import *


# ================== Views ===============================================

class ResultsView(View):
    def get(self, request, index_num):
        student = get_object_or_404(Student, index_number = index_num)
        data_set = student.studentsresults_set.all().order_by('-date')[0]
        # data = data_set.data
        comments = checkExcersice(data_set)
        # comments = data_set.report
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
        print(form.non_field_errors())
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # name = form.cleaned_data['name']
            # last_name = form.cleaned_data['last_name']
            User.objects.create_user(username = username, password= password)
            return redirect('raw_login')
        else:
            return render(request, "networks/index.html", {'form':form})
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
                print(student.index_number)
                student_results = StudentsResults(index_number=student)
                for i in range(0, len(ranges)):
                    j = i + 3 # field in StudentsResults index
                    value = readExcercise(filename, ranges[i])
                    setattr(student_results, fields[j].name, value)
                student_results.save()
                return redirect("student")
            except:
                return HttpResponse(self.get(request))

        if button == 'get_data':
            index_num = int(username)
            set_number = Student.objects.get(index_number=index_num).RW_set_number
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

        if button == 'profile':
            return redirect('/student/')

class GWView(LoginRequiredMixin,View):
    def get(self, request):
        title = 'Automatyczny sprawdzacz ćwiczeń'
        return render(request, 'networks/GW.html', {'title': title})

    def post(self, request):
        username = request.user.username
        title = 'Automatyczny sprawdzacz ćwiczeń'
        button = request.POST.get('button')

        if button == 'get_data':
            return redirect('GW_data')

        if button == 'profile':
            return redirect('/student/')

        if button == 'send_results':
            return redirect('GW_exercises')

class StudentView(View):
    def get(self, request):
        username = request.user.username
        student = get_object_or_404(Student, index_number = int(username))
        student_results_raw = StudentsResults.objects.filter(index_number=student)

        return render(request, 'networks/student.html', {'student':student, 'raw_results':student_results_raw})

    def post(self, request):
        button = request.POST.get('report_button')
        results = StudentsResults.objects.get(pk = int(button))
        if results.report is None:
            results.report = checkExcersice(results)
            results.save()
        report = results.report

        text = ''
        for item in report:
            text += f'{item} \n'

        filename = f'Raport_{results.date}.txt'
        response = HttpResponse(text, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
        return response

        # return HttpResponse(report)



class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'networks/login.html', {'form' : form})
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            currUrl = self.request.path
            print(currUrl)

            username = form.cleaned_data['login']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password = password)
            # print(username, password, user)
            if user is not None:
                login(request, user)# udało się sprawdzić użytkownika
                url = request.GET.get("next") if request.GET.get("next") is not None else 'main'
                return redirect(url)
                # return HttpResponse('zalogowany')
            else:
                info = 'Błędny login lub hasło'
                return render(request, 'networks/login.html', {'form': form, 'info': info}) # nie udało się :(
        else:
            return HttpResponse('Nie działa')
            # return render(request, 'exercises/form.html', {'form': form})

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('main')


class GWDataView(LoginRequiredMixin,View):
    def get(self, request):
        username = request.user.username
        student = get_object_or_404(Student, index_number=int(username))
        data = getData(student.GW_set_number)
        ellipsoid = GRS80()
        return render(request, 'networks/GW_data.html', {'data':data, 'ellipsoid':ellipsoid})

class GWExercisesView(View):
    def get(self, request):
        return render(request, 'networks/GW_exercises.html')




