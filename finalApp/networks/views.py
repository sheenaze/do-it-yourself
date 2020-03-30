# ========  external libraries ==================
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from networks.leveling.check import *
from networks.geodesy.check_algorithms import *

# ========  my files ==================
from .forms import *
# from geodesy.algorithms import *
from networks.geodesy.geodesy_exercises import *


# ================== Views ===============================================
class ResultsView(View):
    def get(self, request, index_num):
        student = get_object_or_404(Student, index_number=index_num)
        data_set = student.studentsresults_set.all().order_by('-date')[0]
        comments = checkExcersice(data_set)
        return render(request, 'networks/results.html', {'comments': comments})


class MainView(View):
    def get(self, request):
        form = AddUserForm()
        title = 'Serwis do samodzielnego sprawdzania ćwiczeń'
        return render(request, 'networks/index.html', {'form': form, 'title': title})

    def post(self, request):
        form = AddUserForm(request.POST)
        print(form.non_field_errors())
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            User.objects.create_user(username=username, password=password)
            return redirect('login')
        else:
            return render(request, "networks/index.html", {'form': form})


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
                student = Student.objects.get(index_number=index_num)
                print(student.index_number)
                student_results = StudentsResults(index_number=student)
                for i in range(0, len(ranges)):
                    j = i + 3  # field in StudentsResults index
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
            path = "excel_files/RaW1_Imie_Nazwisko.xlsx"  # './%s_Report.xlsx' % id  # this should live elsewhere, definitely
            filename = 'RaW1_Imie_Nazwisko.xlsx'
            with open(path, "rb") as excel:
                data = excel.read()
            response = HttpResponse(data,
                                    content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = f'attachment; filename= {filename}'
            return response

        if button == 'profile':
            return redirect('/student/')


class GWView(LoginRequiredMixin, View):
    def get(self, request):
        title = 'Automatyczny sprawdzacz ćwiczeń'
        return render(request, 'networks/GW.html', {'title': title})

    def post(self, request):
        username = request.user.username
        button = request.POST.get('button')

        if button == 'get_data':
            return redirect('GW_data')

        if button == 'profile':
            return redirect('/student/')

        if button == 'send_results':
            return redirect('GW_exercises')


class StudentView(LoginRequiredMixin, View):
    def get(self, request):
        username = request.user.username
        student = get_object_or_404(Student, index_number=int(username))
        student_results_raw = StudentsResults.objects.filter(index_number=student)

        return render(request, 'networks/student.html', {'student': student, 'raw_results': student_results_raw})

    def post(self, request):
        button = request.POST.get('report_button')
        results = StudentsResults.objects.get(pk=int(button))
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
        return render(request, 'networks/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['login']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)  # udało się sprawdzić użytkownika
                url = request.GET.get("next") if request.GET.get("next") is not None else 'main'
                return redirect(url)
            else:
                info = 'Błędny login lub hasło'
                return render(request, 'networks/login.html', {'form': form, 'info': info})  # nie udało się :(
        else:
            return HttpResponse('Nie działa')
            # return render(request, 'exercises/form.html', {'form': form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('main')


class GWDataView(LoginRequiredMixin, View):
    def get(self, request):
        username = request.user.username
        student = get_object_or_404(Student, index_number=int(username))
        data = get_data(student.GW_set_number)
        ellipsoid = GRS80()
        return render(request, 'networks/GW_data.html', {'data': data, 'ellipsoid': ellipsoid})


class GWExercisesView(View):
    def get(self, request):
        return render(request, 'networks/GW_exercises.html')


# class GWExercise_2View(View):
#     def get(self, request):
#         form = Exercise_2Form()
#         return render(request, f'networks/exercise_2.html', {'form': form})
#     def post(self, request, ex_number=0):
#         form = Exercise_2Form(request.POST)
#         username = request.user.username
#         student = get_object_or_404(Student, index_number = username)
#         id = student.pk
#         set_num = student.GW_set_number
#         if form.is_valid():
#             CA = [form.cleaned_data['XA'], form.cleaned_data['YA'], form.cleaned_data['ZA']]
#             measurements = [form.cleaned_data['distance'], form.cleaned_data['zenith'], form.cleaned_data['azimuth']]
#             latA = form.cleaned_data['FiA_D']+form.cleaned_data['FiA_M']/60+form.cleaned_data['FiA_S']/3600
#             lonA = form.cleaned_data['LbdA_D']+form.cleaned_data['LbdA_M']/60+form.cleaned_data['LbdA_S']/3600
#             HA = form.cleaned_data['HA']
#             neu =[form.cleaned_data['neu_n'], form.cleaned_data['neu_e'], form.cleaned_data['neu_u']]
#             dXAB =[form.cleaned_data['dX_AB'], form.cleaned_data['dY_AB'], form.cleaned_data['dZ_AB']]
#             D = [[form.cleaned_data['D11'], form.cleaned_data['D12'], form.cleaned_data['D13']],
#                  [form.cleaned_data['D21'], form.cleaned_data['D22'], form.cleaned_data['D23']],
#                  [form.cleaned_data['D31'], form.cleaned_data['D32'], form.cleaned_data['D33']]]
#             CB = [form.cleaned_data['XB'], form.cleaned_data['YB'], form.cleaned_data['ZB']]
#             latB = form.cleaned_data['FiB_D']+form.cleaned_data['FiB_M']/60+form.cleaned_data['FiB_S']/3600
#             lonB = form.cleaned_data['LbdB_D']+form.cleaned_data['LbdB_M']/60+form.cleaned_data['LbdB_S']/3600
#             HB = form.cleaned_data['HB']
#
#             Exercise2.objects.create(index_number_id=id, set_num=set_num, XYZ_A=CA, measurements=measurements, lon_lat_H_A=[latA, lonA, HA],
#                                                 neu_AB=neu, dX_AB=dXAB, D_matrix=D, XYZ_B=CB, lon_lat_H_B=[latB, lonB, HB])
#
#         return HttpResponse('jestem w poście')

class HirvonenView(View):
    def get(self, request):
        form = HirvonenForm()
        path = request.path
        if 'Hirvonen' in path:
            return render(request, 'networks/hirvonen.html', {'form': form})
        elif "LonLatH2XYZ" in path:
            return render(request, 'networks/LonLatH2XYZ.html', {'form': form})

    def post(self, request):
        form = HirvonenForm(request.POST)
        if form.is_valid():
            x = form.cleaned_data['XA']
            y = form.cleaned_data['YA']
            z = form.cleaned_data['ZA']
            fi_deg = form.cleaned_data['FiA_D'] + form.cleaned_data['FiA_M'] / 60 + form.cleaned_data['FiA_S'] / 3600
            lbd_deg = form.cleaned_data['LbdA_D'] + form.cleaned_data['LbdA_M'] / 60 + form.cleaned_data[
                'LbdA_S'] / 3600
            height = form.cleaned_data['HA']
            path = request.path
            if 'Hirvonen' in path:
                message = check_hirvonen(x, y, z, fi_deg, lbd_deg, height, GRS80)
                return render(request, 'networks/hirvonen.html', {'form': form, 'message': message})
            elif "LonLatH2XYZ" in path:
                message = check_fi_lbd_h_to_xyz(fi_deg, lbd_deg, height, x, y, z, GRS80)
                return render(request, 'networks/LonLatH2XYZ.html', {'form': form, 'message': message})

class NeuXYZ_View(View):
    def get(self, request):
        form = NeuXYZ_Form()
        path = request.path
        if 'XYZ_to_neu' in path:
            return render(request, 'networks/XYZ_to_neu.html', {'form': form})
        elif 'neu_to_XYZ' in path:
            return render(request, 'networks/neu_to_XYZ.html', {'form': form})

    def post(self, request):
        form = NeuXYZ_Form()
        path = request.path
        if form.is_valid():
            dX = form.cleaned_data['dX']
            dY = form.cleaned_data['dY']
            dZ = form.cleaned_data['dZ']
            north = form.cleaned_data['north']
            east = form.cleaned_data['east']
            up = form.cleaned_data['up']
            fi_deg = form.cleaned_data['FiA_D'] + form.cleaned_data['FiA_M'] / 60 + form.cleaned_data['FiA_S'] / 3600
            lbd_deg = form.cleaned_data['LbdA_D'] + form.cleaned_data['LbdA_M'] / 60 + form.cleaned_data[
                'LbdA_S'] / 3600

            if 'XYZ_to_neu' in path:
                message = check_NEU_XYZ(dX, dY, dZ, north, east, up, fi_deg, lbd_deg, Neu2XYZ=False)
                return render(request, 'networks/XYZ_to_neu.html', {'form': form, 'message':message})
            elif 'neu_to_XYZ' in path:
                message = check_NEU_XYZ(dX, dY, dZ, north, east, up, fi_deg, lbd_deg, Neu2XYZ=True)
                return render(request, 'networks/neu_to_XYZ.html', {'form': form, 'message':message})