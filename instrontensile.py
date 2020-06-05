import pandas as pd
import re
import csv
import matplotlib.pyplot as pyplt
import os
import openpyxl
from openpyxl import Workbook, load_workbook

Tensile = 'File Name \t UTS (MPa) \n'
'''get file locations of the raw .csv file for '''
for i in range(0, 4):
    dose = ['0.1MGy_', '0.2MGy_', '0.5MGy_', '1.0MGy_']
    file_front = 'data/' + str(dose[i])
    # print(file_front)
    for j in range(0,2):
        thickness = ['5layer_1.23.2020.Specimen_RawData_', '13layer_1.23.2020.Specimen_RawData_']
        file_middle = file_front + str(thickness[j])
        # print(file_middle)
#        for k in range(0,2):
#            type = ['typei', 'typeiv']
#            file_back = file_middle + str(type[k])
#            for n in range(0, 2):
#                raster = ['_4545_', '_090_']
#                file_last = file_back + str(raster[n]) + 'r('
        for replicates in range(1, 4):
            file = file_middle + str(replicates) + '.csv'
            print(file)
            split_filename = file.split('_')
            specimen_type = split_filename[1]
            printer = split_filename[2]
           # layer = split_filename[0]
           # split_layer = layer.split('/')
           # layer_thickness = split_layer[1]
           # infill = split_filename[1]
            g_len = 25  # mm
            if specimen_type in ['5layer']:
                '''5 layer cross-sectional area'''
                area = 6* 1.36  # cm^2
            else:
                '''13 layer cross section area'''
                area = 6*3.3302 # cm^2

                # print('The '+str(specimen_type)+' cross-sectional area is', area, ' mm2')
                # print('The '+str(specimen_type)+' gage length is', g_len, ' mm')
                '''get file name to write output file'''
                file_name = os.path.splitext(file)[0]
                file_name = os.path.basename(file_name)
                # print(file_name)
            data=pd.read_csv(file)
            data.head()