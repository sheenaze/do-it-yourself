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

root = Tk()
root.title('My final app')

root.filename = filedialog.askopenfilename(initialdir = '../excel_files')
print (root.filename)

# readExcercise(root.filename, ranges[0])
xls_file = xlrd.open_workbook(root.filename)
sheet = xls_file.sheet_by_index(0)
cells = excelRanges('A23:G36')
rows_num = cells[1] - cells[0] + 1
columns_num = cells[3] - cells[2] + 1
matrix = np.zeros((rows_num, columns_num))

print(matrix)
print(rows_num)
print(columns_num)
print(cells)

for i in range(cells[0], cells[1]+1):
    for j in range(cells[2], cells[3]+1):
        matrix[i-cells[0],j-cells[2]] = sheet.cell_value(i, j)

print(matrix)

# def readExcercise(filename, range):
#     cells = excelRanges(range)
#     xls_file = xlrd.open_workbook(filename)
#     sheet = xls_file.sheet_by_index(0)
#     rows_num = cells[1]-cells[0]+1
#     columns_num = cells[3]-cells[2]+1
#     matrix = np.empty((rows_num, columns_num))
#     for i in range(cells[0], cells[1]+1):
#         for j in range(cells[2], cells[3]+1):
#             matrix[i,j] = sheet.cell_value(i, j)
#
#     print(matrix)
#     return matrix
#
# readExcercise(root.filename, 'A23:G36')




