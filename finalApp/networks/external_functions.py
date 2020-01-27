import string
from tkinter import Tk, filedialog
import xlrd
import numpy as np

ranges = [
    'C2:C2', #set number
    'B6:D19', #raw data
    'A23:G36', #A
    'A39:N52', #LP
    'H23:H36'# L
    'A57:G63', #ATPA
    'H57:H63', #ATPL
    'C69:C75', #x
    'G69:G82', #V
    'D69:D75', #HW
    'H69:H82', #ObsW
    'C88:C88', #sig_0
    'F90:F96', #mx
    'G90:G103' #mv
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
        print('Wprowadzony zakres nie jest zakresem komórek Excela')


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
    for i in range(cells[0], cells[1] + 1):
        for j in range(cells[2], cells[3] + 1):
            matrix[i - cells[0], j - cells[2]] = sheet.cell_value(i, j)

    print(matrix)
    return matrix



