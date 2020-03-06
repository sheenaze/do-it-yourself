import os
from django.shortcuts import get_object_or_404
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finalApp.settings')
import django
django.setup()

from .external_functions import *


def thirdStage(comments, set_num, real_data, consts, query_set):
    comments.append("======================== Etap III ========================")
    points = getAllPoints(set_num)
    real_network = createLevelingObject(real_data, consts, points, set_num)

    counter = 0

    sigma0 = query_set.sig_0
    sigma0_my = real_network.sigma0()

    if np.round(sigma0, 7) == np.round(sigma0_my, 7):
        counter += 1
        mx = np.array(query_set.mx_matrix)
        mx_test = real_network.mx_vector()

        cond_mx1 = np.all(np.round(mx, 7) == np.round(mx_test, 7))
        cond_mx2 = np.all(np.round(mx / 1000, 7) == np.round(mx_test, 7))

        if np.any([cond_mx1, cond_mx2]):
            counter += 1
            comments.append('Błędy wyrównanwych wysokości są poprawne.')
        elif np.all(mx == np.zeros(np.shape(mx))):
            comments.append('Błędy wyrównanych wysokości nie zostały wprowadzone.')
        elif np.sum(cond_mx1) >= np.sum(cond_mx2):
            rows = failedRows(cond_mx1)
            comments.append(f"Błędy wyrównanych wysokości są niepoprawne. Sprawdzić wiersze nr: {rows}")
        else:
            rows = failedRows(cond_mx2)
            comments.append(f"Błędy wyrównanych wysokości. Sprawdzić wiersze nr: {rows}")

        mV = np.array(query_set.mV_matrix)
        mV_test = real_network.mV_vector()

        cond_mV1 = np.all(np.round(mV, 7) == np.round(mV_test, 7))
        cond_mV2 = np.all(np.round(mV / 1000, 7) == np.round(mV_test, 7))

        if np.any([cond_mV1, cond_mV2]):
            counter += 1
            comments.append('Błędy poprawek obserwacyjnych są poprawne.')
        elif np.all(mV == np.zeros(np.shape(mV))):
            comments.append('Błędy poprawek obserwacyjnych nie zostały wprowadzone.')
        elif np.sum(cond_mV1) >= np.sum(cond_mV2):
            rows = failedRows(cond_mV1)
            comments.append(f"Błędy poprawek obserwacyjnych są niepoprawne. Sprawdzić wiersze nr: {rows}")
        else:
            rows = failedRows(cond_mV2)
            comments.append(f"Błędy poprawek obserwacyjnych są niepoprawne. Sprawdzić wiersze nr: {rows}")

    else:
        comments.append(
            'Błąd średni typowego spostrzeżenia jest niepoprawny. Dalsza analiza dokładności mija się z celem.')

    if counter == 3:
        comments.append('Ćwiczenie zaliczone.')
    else:
        comments.append('Ćwiczenie do poprawy.')
    return comments