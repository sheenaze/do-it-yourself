"""finalApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from networks.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainView.as_view(), name = 'main'),
    # path('student/', MainStudentView.as_view(), name = 'main_student'),
    path('results/<int:index_num>', ResultsView.as_view(), name='results'),
    path('RaW/', RaWView.as_view(), name = 'RaW_main'),
    path('GW/', GWView.as_view(), name = 'GW_main'),
    path('login/', LoginView.as_view(), name = 'login'),
    path('student/', StudentView.as_view(), name = 'student'),
    path('logout/', LogoutView.as_view(), name = 'logout'),
    path('GW_data/', GWDataView.as_view(), name = 'GW_data'),
    path('GW_exercises/', GWExercisesView.as_view(), name = 'GW_exercises'),
    path('GW_exercises/Hirvonen/', HirvonenView.as_view(), name = 'Hirvonen'),
    path('GW_exercises/LonLatH2XYZ/', HirvonenView.as_view(), name = 'LonLat'),
    path('GW_exercises/XYZ_to_neu/', NeuXYZ_View.as_view(), name = 'xyz2neu'),
    path('GW_exercises/neu_to_XYZ/', NeuXYZ_View.as_view(), name = 'neu2xyz'),
]
