import os
from django.shortcuts import get_object_or_404
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finalApp.settings')
import django
django.setup()

import string
from tkinter import Tk, filedialog
import xlrd
import numpy as np


import numpy as np
from networks.models import *
from networks.functions_and_classes.leveling import *
from networks.functions_and_classes.stage_first import *


def validate_empty(value):
    if value is not "":
        return value
    else:
        return 1000000

ranges = [
    'C2:C2', #set number
    'A6:D19', #raw data
    'G6:H12' , # estH
    'A23:G36', #A
    'A39:N52', #LP
    'H23:H36',# L
    'A57:G63', #ATPA
    'H57:H63', #ATPL
    'C69:C75', #x
    'G69:G82', #V
    'D69:D75', #HW
    'H69:H82', #ObsW
    'F90:F96', #mx
    'G90:G103', #mv
    'C88:C88',  # sig_0
]


def open():
    """
    function opens a dialog window
    :return: name of opened file
    """
    root = Tk()
    root.title('My final app')
    root.filename = filedialog.askopenfilename()
    root.destroy()
    return root.filename

#converting string to row and column numbers, works only for columns A to Z
def excelRanges(excel_range):
    """
    :param excel_range: range of excel cells e.g. 'A23:G36'
    :return: list of rows and columns integer numbers
    REMARK: works only for columns A to Z
    """
    try:
        letters = list(string.ascii_uppercase)
        ind = excel_range.index(':')
        col1 = letters.index(excel_range[0])
        col2 = letters.index(excel_range[ind+1])
        row1 = int(excel_range[1:ind])-1
        row2 = int(excel_range[ind+2:])-1
        if col2>=col1 and row2>=row1:
            return [row1, row2, col1, col2]
        else:
            print('Wprowadzony zakres jest niepoprawny')
    except:
        print(f'Wprowadzony zakres {excel_range} nie jest zakresem komórek Excela')


def readExcercise(filename, excel_range):
    """
    :param filename: name of excel file to read
    :param range: raange of cells in string format, e.g. 'A23:G36'
    :return: data from the indicated file and range as an array
    """
    xls_file = xlrd.open_workbook(filename)
    sheet = xls_file.sheet_by_index(0)
    cells = excelRanges(excel_range)
    rows_num = cells[1] - cells[0] + 1
    columns_num = cells[3] - cells[2] + 1
    matrix = np.zeros((rows_num, columns_num))
    try:
        if rows_num == 1 and columns_num == 1:
            matrix = validate_empty(sheet.cell_value(cells[0], cells[2]))
            return matrix
        else:
            for i in range(cells[0], cells[1] + 1):
                for j in range(cells[2], cells[3] + 1):
                    matrix[i - cells[0], j - cells[2]] = sheet.cell_value(i, j)
            return matrix.tolist()#.tostring()
    except:
        return matrix.tolist()#.tostring()



# functions
# def savePoint(num, H, set_num):
#     Points.objects.create(point = num, height = H, network_name=set_num)
#
# def gettingRealData(set_num):
#     real_data_set = Leveling.objects.filter(network_name = set_num)
#     real_data = []
#     for item in real_data_set:
#         insert = [int(item.obs_number), int(item.start_point), int(item.end_point), item.observation, item.accuracy]
#         real_data.append(insert)
#     return np.array(real_data)
#
# def constPoints():
#     const_set = Consts.objects.all()
#     constPoints = []
#     for item in const_set:
#         insert = [int(item.point), item.height]
#         constPoints.append(insert)
#     return np.array(constPoints)
#
# def getAllPoints(set_num):
#     points_set = Points.objects.filter(network_name = set_num)
#     if len(points_set) == 0:
#         return None
#     else:
#         points = []
#         for item in points_set:
#             insert = [float(item.point), item.height]
#             points.append(insert)
#         return np.array(points)
#
# def createLevelingObject(data, consts, points, set_num):
#     if points is None:
#         real_network = LevelingAdjustment(data, consts)
#         points = real_network.points_height()
#
#         for point in points:
#             savePoint(point[0], point[1], set_num)
#     else:
#         real_network = LevelingAdjustment(data, consts, points)
#
#     return real_network
#
# def matrixInRangeValidation(pattern, matrix2validate, value):
#     return np.all(pattern-value <= matrix2validate) and np.all(pattern+value >= matrix2validate)
#
#
# def failedRows(matrix):
#     rows = []
#     for ind in range(0, len(matrix)):
#         if sum(matrix[ind, :]) != np.shape(matrix)[1]:
#             rows.append(ind + 1)
#     return rows


