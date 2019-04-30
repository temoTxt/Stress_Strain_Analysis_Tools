import pandas as pd
import re
import csv
import matplotlib.pyplot as plt
import os
import openpyxl
from openpyxl import Workbook, load_workbook

AppliedStress = 'Layer \t Infill \t Percent UTS \t Applied Stress (MPa) \n'
'''calculate the applied stress for d3039 specimens at 4545 raster for 4 build configurations'''
for n in range(0, 4):
    percent_uts = [.95, .85, .75, .65]
    #d3039_uts = [26.09, 25.37, 23.55, 21.25]
    applied_stress1 = round(26.09 * percent_uts[n], 1)
    print(applied_stress1)
    applied_stress2 = round(25.37 * percent_uts[n], 1)
    print(applied_stress2)
    applied_stress3 = round(23.55 * percent_uts[n], 1)
    print(applied_stress3)
    applied_stress4 = round(21.25 * percent_uts[n], 1)
    print(applied_stress4)
    AppliedStress1 = '0.254 \t solid \t' + str(percent_uts[n]) + '\t' + str(applied_stress1) + '\n'
    AppliedStress2 = '0.3302 \t solid \t' + str(percent_uts[n]) + '\t' + str(applied_stress2) + '\n'
    AppliedStress3 = '0.254 \t hd \t' + str(percent_uts[n]) + '\t' + str(applied_stress3) + '\n'
    AppliedStress4 = '0.3302 \t hd \t' + str(percent_uts[n]) + '\t' + str(applied_stress4) + '\n'
    AppliedStress = AppliedStress + AppliedStress1 + AppliedStress2 + AppliedStress3 + AppliedStress4
print(AppliedStress)
d3039appliedstress_data = open('data/appliedstress_d3039_4545', 'r+')
d3039appliedstress_data.writelines(AppliedStress)
