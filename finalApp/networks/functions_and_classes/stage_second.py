import os
from django.shortcuts import get_object_or_404
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finalApp.settings')
import django
django.setup()

# import numpy as np
from .external_functions import *

def secondStage(data, HP, query_set, comments, network_student):
    comments.append("======================== Etap II ========================")

    x = np.array(query_set.x_matrix)
    x_test = network_student.x_vector()

    cond_x1 = np.round(x, 9) == np.round(x_test, 9)
    cond_x2 = np.round(x / 1000, 9) == np.round(x_test, 9)

    counter = 0

    if np.any([np.all(cond_x1), np.all(cond_x2)]):
        comments.append('Wektor niewiadomych x jest poprawny.')
        counter += 1


        HW = np.array(query_set.HW_matrix)
        HW_test = network_student.HW_vector()


        if np.all(np.round(HW, 9) == np.round(HW_test[:,-1], 9).reshape((len(HW_test),1))):
            comments.append('Wektor wyrównanych wysokości jest poprawny.')
            counter += 1
        elif np.all(HW == np.zeros(np.shape(HW))):
            comments.append('Wektor wyrównanych wysokości nie został wprowadzony.')
        else:
            comments.append('Wektor wyrównanych wysokości jest niepoprawny.')

        V = np.array(query_set.V_matrix)
        V_test = network_student.V_vector()
        cond_V1 = np.round(V, 9) == np.round(V_test, 9)
        cond_V2 = np.round(V / 1000, 9) == np.round(V_test, 9)


        if np.any([np.all(cond_V1), np.all(cond_V2)]):
            comments.append('Wektor poprawek obserwacyjnych V jest poprawny.')
            counter += 1


            dhW = np.array(query_set.dhW_matrix)
            dhW_test = network_student.obsW_matrix()[:,-1]

            if np.all(np.round(dhW, 9) == np.round( dhW_test, 9).reshape((len(dhW_test),1))):
                comments.append('Wektor wyrównanych obserwacji jest poprawny.')
                counter += 1

            elif np.all(dhW == np.zeros(np.shape(dhW))):
                 comments.append('Wektor wyrównanych obserwacji nie został wprowadzony')
            else:
                comments.append('Wektor wyrównanych obserwacji jest niepoprawny.')

        elif np.all(V == np.zeros(np.shape(V))):
            comments.append('Wektor poprawek do wysokości  V nie został wprowadzony.')
        else:
            comments.append('Wektor poprawek obserwacyjnych V jest niepoprawny.')


        if counter != 4:
            comments.append('Etap II nie został wykonany poprawnie, analiza dokładności nie zostanie wykonana.')
        else:
            comments.append('Przechodzę do III etapu.')
        return comments


    else:
        ATPA = np.array(query_set.ATPA_matrix)
        ATPL = np.array(query_set.ATPL_matrix)

        ATPA_test = network_student.ATPA_matrix()
        ATPL_test = network_student.ATPL_matrix()

        if np.all(ATPA == ATPA_test) and np.all(ATPL == ATPL_test):
            comments.append('Macierze ATPA i ATPL są poprawne')
        elif not np.all(ATPA == ATPA_test):
            comments.append(
                'Macierz ATPA nie jest spójna z danymi wyjściowymi. Sprawdzić czy do obliczeń wzięte zostały właściwe macierze.')
        elif not np.all(ATPL == ATPL_test):
            comments.append(
                'Macierz ATPL nie jest spójna z danymi wyjściowymi. Sprawdzić czy do obliczeń wzięte zostały właściwe macierze.')
        comments.append('Wektor niewiadomych jest niepoprawny lub nie został wprowadzony, dalsze sprawdzanie mija się z celem')
        return comments

