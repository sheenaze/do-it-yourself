import string

import numpy as np
import pandas as pd
# -*- coding: utf-8 -*-
import xlwt
from tkinter import *
from tkinter import filedialog
import xlrd
from xlrd.timemachine import xrange
from external_functions import *
# from networks.models import *
#
# matrix = [0, 1, 2]
# str = f''
# for field in StudentsResults._meta.fields:
#     str.join(f'{field.name}={matrix}')
#
# print(str)


root = Tk()
root.title('My final app')

root.filename = filedialog.askopenfilename(initialdir = '../excel_files')
print (root.filename)

xls_file = xlrd.open_workbook(root.filename)
sheet = xls_file.sheet_by_index(0)
print(root.filename)
# fields = Leveling._meta.fields

# for i in range(0,840):
#     print([sheet.cell_value(i, 0), sheet.cell_value(i, 1), sheet.cell_value(i, 2), sheet.cell_value(i, 3), sheet.cell_value(i, 4), sheet.cell_value(i, 5)], i)
#     Leveling.objects.create(network_name = str(int(sheet.cell_value(i, 0))),
#                             obs_number = int(sheet.cell_value(i, 1)),
#                             start_point = str(int(sheet.cell_value(i,2))),
#                             end_point = str(int(sheet.cell_value(i,3))),
#                             observation = float(sheet.cell_value(i,4)),
#                             accuracy = float(sheet.cell_value(i,5)))
    # object = Leveling()
    # for j in range(0,5):
    #     value = sheet.cell_value(i, j)
    #     # print(value)
    #     setattr(object, fields[j+1].name, value)


# # readExcercise(root.filename, ranges[0])
# xls_file = xlrd.open_workbook(root.filename)
# sheet = xls_file.sheet_by_index(0)
# cells = excelRanges('C2:C2')
# rows_num = cells[1] - cells[0] + 1
# columns_num = cells[3] - cells[2] + 1
# matrix = np.zeros((rows_num, columns_num))
#
# print(matrix)
# print(rows_num)
# print(columns_num)
# print(cells)
#
# for i in range(cells[0], cells[1]+1):
#     for j in range(cells[2], cells[3]+1):
#         matrix[i-cells[0],j-cells[2]] = sheet.cell_value(i, j)
#
# print(matrix)
#
# def readExcercise1(filename,  excel_range):
#     xls_file = xlrd.open_workbook(filename)
#     sheet = xls_file.sheet_by_index(0)
#     cells = excelRanges(excel_range)
#     rows_num = cells[1] - cells[0] + 1
#     columns_num = cells[3] - cells[2] + 1
#     matrix = np.zeros((rows_num, columns_num))
#     for i in range(cells[0], cells[1] + 1):
#         for j in range(cells[2], cells[3] + 1):
#             matrix[i - cells[0], j - cells[2]] = sheet.cell_value(i, j)
#
#     print(matrix)
#     return matrix
# #
# print(readExcercise1(root.filename, 'A23:G36'))




