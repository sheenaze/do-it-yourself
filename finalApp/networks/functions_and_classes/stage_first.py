import os
from django.shortcuts import get_object_or_404
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finalApp.settings')
import django
django.setup()

# import numpy as np
from .external_functions import *

def firstStage(data, set_num,real_data, A, P, L, HP ):
    comments = ["======================== Etap I ========================"]
    if np.all(real_data[:,-1] == data[:,-1]):
        # correct data, I'm getting further
        consts = constPoints()  # now I need to get to the const points, also I can prepare the rigth object, but first I need to know if I have already points or I need to estaablish them
        points = getAllPoints(set_num)  # I need to have all points, here I check if I can take them from a database
        real_network = createLevelingObject(real_data, consts, points,set_num)  # here I prepare the LeveligAdjustment object

        # now I can start comparing Hprz, A, P and L matrices
        A_real = real_network.A_matrix()

        P_real = real_network.P_matrix()
        H_real = real_network.points_height()

        A_condition = A == A_real

        cond_p1 = np.round(P, 9) == np.round(P_real, 9)
        cond_p2 = np.round(P * 10 ** 6, 7) == np.round(P_real, 7)
        P_conditions = [np.all(cond_p1), np.all(cond_p2)]

        Hp_condition = matrixInRangeValidation(H_real[:, 1], HP[:, 1], 0.100)

        if all([np.all(A_condition), np.any(P_conditions), Hp_condition]):
            # if np.all(cond_p2):
            #     P = np.round(P * 10 ** 6, 7)

            for comment in ['Wspólrzędne przybliżone poprawne', 'Macierz A w porządku', 'Macierz P w porządku']:
                comments.append(comment)

            network_student = LevelingAdjustment(data, consts, HP)
            L_test = network_student.L_vector()
            cond_l1 = (np.round(L, 9) == np.round(L_test, 9))
            cond_l2 = (np.round(L / 1000, 9) == np.round(L_test, 9))

            if np.any([np.all(cond_l1), np.all(cond_l2)]):
                comments.append('Wektor wyrazów wolnych poprawny')
                comments.append('Przechodzę do etapu II')
                # here I should stop computing if only the first part is chosen to be checked
                # if np.all(cond_l2):
                #     L = np.round(L / 1000, 9)


            else:
                if sum((cond_l1)) >= sum(cond_l2):
                    rows = failedRows(cond_l1)
                    comments.append(f"Wektor wyrazów wolnych niepoprawny. Sprawdzić wiersze: {rows}")
                else:
                    rows = failedRows(cond_l2)
                    comments.append(f"Wektor wyrazów wolnych niepoprawny. Sprawdzić wiersze: {rows}")

                comments.append('Wektor wyrazów wolnych jest niepoprawny, dalsze sprawdzanie mija się z celem')
                return comments


        # If some of them are not good I need to stop evaluation here
        else:
            if not Hp_condition:
                if np.all(HP == np.zeros(np.shape(HP))):
                    comments.append(f"Współrzędne przybliżone nie zostały poprawnie wprowadzone")
                else:
                    cond_matrix = np.abs(HP - H_real) > 0.100
                    rows = failedRows(cond_matrix)
                    comments.append(f"Coś nie tak ze współrzędnymi przybliżonymi. Sprawdzić wiersze nr: {rows}")
            else:
                comments.append('Współrzędne przybliżone ok')
                network_student = LevelingAdjustment(data, consts, HP)
                L_test = network_student.L_vector()
                cond_l1 = (np.round(L, 9) == np.round(L_test, 9))
                cond_l2 = (np.round(L / 1000, 9) == np.round(L_test, 9))

                if not np.any([np.all(cond_l1), np.all(cond_l2)]):

                    if sum((cond_l1)) >= sum(cond_l2):
                        rows = failedRows(cond_l1)
                        comments.append(f"Wektor wyrazów wolnych niepoprawny. Sprawdzić wiersze: {rows}")
                    else:
                        rows = failedRows(cond_l2)
                        comments.append(f"Wektor wyrazów wolnych niepoprawny. Sprawdzić wiersze: {rows}")

            if not np.all(A_condition):
                if np.all(A == np.zeros(np.shape(A))):
                    comments.append(f"Macierz A nie została poprawnie wprowadzona")
                else:
                    rows = failedRows(A_condition)
                    comments.append(f"Coś nie tak z macierzą A. Sprawdzić wiersze nr: {rows}")
            else:
                comments.append('Macierz A w porządku')

            if not np.any(P_conditions):
                if np.all(P == np.zeros(np.shape(P))):
                    comments.append(f"Macierz P nie została poprawnie wprowadzona")
                elif np.sum(cond_p1) >= np.sum(cond_p2):
                    rows = failedRows(cond_p1)
                    comments.append(f"Coś nie tak z macierzą P. Sprawdzić wiersze nr: {rows}")
                else:
                    rows = failedRows(cond_p2)
                    comments.append(f"Coś nie tak z macierzą P. Sprawdzić wiersze nr: {rows}")
            else:
                comments.append('Macierz P w porządku')

            comments.append('Dalsze sprawdzanie mija się z celem.')
        return comments

    else:
        comments.append(f'Zostały wzięte niewłaściwe dane, dalsze sprawdzanie mija się z celem')
        return comments
