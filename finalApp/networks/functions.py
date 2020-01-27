import string
from tkinter import Tk, filedialog
import xlrd
import numpy as np

ranges = [
    ('A23:G36'), #A
    ('A39:N52'), #LP
    ('H23:H36')# L
]


def open():
    root = Tk()
    root.title('My final app')
    root.filename = filedialog.askopenfilename()
    root.destroy()
    return root.filename


def excelRanges(excel_range):
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
        print('Wprowadzony zakres nie jest zakresem komórek Excela')


def readExcercise(filename, range):
    cells = excelRanges(range)
    xls_file = xlrd.open_workbook(filename)
    sheet = xls_file.sheet_by_index(0)
    rows_num = cells[1]-cells[0]+1
    columns_num = cells[3]-cells[2]+1
    matrix = np.empty((rows_num, columns_num))
    for i in range(cells[0], cells[1]+1):
        for j in range(cells[2], cells[3]+1):
            matrix[i,j] = sheet.cell_value(i, j)

    print(matrix)
    return matrix
