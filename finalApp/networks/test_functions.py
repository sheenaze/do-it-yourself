import string

import numpy as np
import pandas as pd
# -*- coding: utf-8 -*-
import xlwt
from tkinter import *
from tkinter import filedialog
import xlrd
from xlrd.timemachine import xrange

root = Tk()
root.title('My final app')

root.filename = filedialog.askopenfilename(initialdir = '/home/monika/pulpit')
print (root.filename)






