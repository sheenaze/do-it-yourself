import os
from django.shortcuts import get_object_or_404
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finalApp.settings')
import django
django.setup()

# import numpy as np
# from networks.models import *
# from networks.functions_and_classes.leveling import *
# from networks.functions_and_classes.external_functions import *
from networks.functions_and_classes.stage_first import *
from networks.functions_and_classes.stage_second import *
from networks.functions_and_classes.stage_third import *

index_num = 555653
student = get_object_or_404(Student, index_number=index_num)
data_set = student.studentsresults_set.all().order_by('-date')[0]
data = data_set.data


# functions: external_functions.py
# firstStage(): stage_first.py
# secondStage(): stage_secnd.py

# the main function
def checkExcersice(query_set):
    # basic data
    set_num = query_set.set_num
    data = np.array(query_set.data)
    HP = np.array(query_set.HP_matrix)
    A = np.array(query_set.A_matrix)
    P = np.array(query_set.P_matrix)
    L = np.array(query_set.L_matrix)

    p = np.diag(P)
    m_ob = np.round(np.sqrt(1 / p),3)
    data = np.append(data, m_ob.reshape((14, 1)), axis=1)

    real_data = gettingRealData(set_num)
    real_data[:,-1] = real_data[:,-1]/1000
    first_stage = firstStage(data, set_num,real_data, A, P, L, HP )

    comments = first_stage

    if comments[-1] == 'Przechodzę do etapu II.':
        network_student = LevelingAdjustment(data, consts, HP)
        comments = secondStage(data, HP, query_set, comments, network_student)

        # I have to add here the column of accuracy, as I don't have an appropriate field in my model
        if comments[-1] == 'Przechodzę do III etapu.':
            comments = thirdStage(comments, set_num, real_data, consts, query_set)

        return comments
    else:
        return comments




        # print("Mogę iść dalej")



    # return comments

    # now I can start checking the data:
    # 1. I need to compare real data and students data:


    # return sum(sum(real_data[:,:-1] == data))





# print(gettingData(data_set))
print(checkExcersice(data_set))



