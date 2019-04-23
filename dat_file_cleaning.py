import pandas as pd
import re
import csv
import matplotlib.pyplot as plt
import os
import openpyxl
from openpyxl import Workbook, load_workbook

Fatigue = 'File Name  Applied Stress  Max Cycles \n'
'''get file locations of the raw .dat file'''
for i in range(0,2):
    layer_height = ['0.3302', '0.254']
    infill_density = ['solid', 'hd']
    type = ['typei', 'd3039']
    file_front = 'data/' + str(layer_height[i]) + '_' + str(infill_density[i])+'_4545_'+str(type[i])
    for j in range (0,4):
        uts_percent =['95%uts','85%uts', '75%uts', '65%uts']
        file_back = file_front + '_' + str(uts_percent[j]) +'_0.25hz_r('
        for replicates in range(1,4):
            file = file_back+str(replicates)+').dat'
            print(file)
            split_filename = file.split('_')
            specimen_type = split_filename[3]
            test_type = split_filename[4]
            layer = split_filename[0]
            split_layer = layer.split('/')
            layer_thickness = split_layer[1]
            infill = split_filename[1]
            frequency = split_filename[5]
            percent_uts = split_filename[4]

            if specimen_type in ['typei']:
                '''D638 type i cross-sectional area'''
                area = 41.6  # cm^2
                '''gauge length'''
                g_len = 50  # mm

            elif specimen_type in ['typeiv']:
                '''D638 type iv cross-sectional area'''
                area = 19.8  # cm^2
                '''gauge length'''
                g_len = 25  # mm
            else:
                '''D3039 cross-sectional area'''
                area = 82.5 # cm^2
                '''D3039 gauge length'''
                g_len = 180  # mm

            print('The '+str(specimen_type)+' cross-sectional area is', area, ' mm2')
            print('The '+str(specimen_type)+' gage length is', g_len, ' mm')
            '''get file name to write output file'''
            file_name = os.path.splitext(file)[0]
            file_name = os.path.basename(file_name)
            print(file_name)

            '''open file as a giant text blob'''
            if os.path.isfile(file):
                # ...
                with open(file, 'r+') as text:
                    pass
                    '''seperate blob into lines of text'''
                    lines = text.readlines()

                    '''create list object to put in only numerical data'''
                    clean_data = []

                    '''go line by line to scrub header data'''
                    for line in lines:

                        '''convert all \t to an actual tab in the data'''
                        line = line.replace('\t', ',')
                        #print(line)

                        '''strip out the \n at the end of each line'''
                        line = line.rstrip()

                        '''check to see if there are any letters in the string. If there are not it must be a data line'''
                        if re.search('[a-zA-Z]', line) == None:

                            '''if there is actually values in the line then we add it to our cleaned data list object'''
                            if len(line) > 4:

                                '''split the line into multiple elements using the comma as the anchor point'''
                                line = line.split(',')

                                '''add this line to the list object for ingest into Pandas'''
                                clean_data.append(line)

                    '''create list of column titles'''
                    if test_type in ['monotonic']:
                        #tensile test data columns
                        col_name = ['Displacement', 'Force', 'Time']
                    else:
                        #fatigue test data columns
                        col_name = ['Force', 'Displacement', 'Time', 'Count']

                    '''create pandas dataframe with the cleaned data'''
                    data = pd.DataFrame(clean_data, columns=col_name)
                    print(data.head())

                    '''change the data from being a string to a float datatype'''
                    data = data.astype(float)

                    '''Stress calculation'''
                    data['Stress'] = data['Force'] / area

                    '''Normalize the Displacement'''
                    data['NormalDisplacement'] = data['Displacement']-data.iloc[0]['Displacement']

                    '''Strain Calculation'''
                    data['Strain'] = data['NormalDisplacement'] / g_len
                    print(data['Strain'])
                    print(data['Stress'])

                    '''calculating applied stress'''

                    for specimen_type in ['typei']:
                        for frequency in ['0.25hz']:
                            for layer_thickness in ['0.254']:
                                for infill in ['solid']:
                                    typei_uts = 29.18 #MPa
                                    if percent_uts in ['95%uts']:
                                        applied_stress = 0.95*typei_uts
                                    elif percent_uts in ['85%uts']:
                                        applied_stress = 0.85*typei_uts
                                    elif percent_uts in ['75%uts']:
                                        applied_stress = 0.75*typei_uts
                                    else:
                                        applied_stress = 0.65*typei_uts
                                    #calculate the maximum number of cycles and applied stress for fatigue data'''
                                    max_cycles = data['Count'].max()
                    for specimen_type in ['typei']:
                        for frequency in ['0.25hz']:
                            for layer_thickness in ['0.3302']:
                                for infill in ['solid']:
                                    typei_uts = 29.18 #MPa
                                    if percent_uts in ['95%uts']:
                                        applied_stress = 0.95 * typei_uts
                                    elif percent_uts in ['85%uts']:
                                        applied_stress = 0.85 * typei_uts
                                    elif percent_uts in ['75%uts']:
                                        applied_stress = 0.75 * typei_uts
                                    else:
                                        applied_stress = 0.65 * typei_uts
                                    #calculate the maximum number of cycles and applied stress for fatigue data'''
                                    max_cycles = data['Count'].max()
                    for specimen_type in ['typei']:
                        for frequency in ['0.25hz']:
                            for layer_thickness in ['0.254']:
                                for infill in ['hd']:
                                    typei_uts = 24.63 #MPa
                                    if percent_uts in ['95%uts']:
                                        applied_stress = 0.95 * typei_uts
                                    elif percent_uts in ['85%uts']:
                                        applied_stress = 0.85 * typei_uts
                                    elif percent_uts in ['75%uts']:
                                        applied_stress = 0.75 * typei_uts
                                    else:
                                        applied_stress = 0.65 * typei_uts
                                    # calculate the maximum number of cycles and applied stress for fatigue data
                                    max_cycles = data['Count'].max()
                    for specimen_type in ['typei']:
                        for frequency in ['0.25hz']:
                            for layer_thickness in ['0.3302']:
                                for infill in ['hd']:
                                    typei_uts = 24.2 #MPa
                                    if percent_uts in ['95%uts']:
                                        applied_stress = 0.95 * typei_uts
                                    elif percent_uts in ['85%uts']:
                                        applied_stress = 0.85 * typei_uts
                                    elif percent_uts in ['75%uts']:
                                        applied_stress = 0.75 * typei_uts
                                    else:
                                        applied_stress = 0.65 * typei_uts
                                    # calculate the maximum number of cycles and applied stress for fatigue data
                                    max_cycles = data['Count'].max()

                    for specimen_type in ['d3039']:
                        for frequency in ['0.25hz']:
                            for layer_thickness in ['0.254']:
                                for infill in ['solid']:
                                    typei_uts = 26.09 #MPa
                                    if percent_uts in ['95%uts']:
                                        applied_stress = 0.95 * typei_uts
                                    elif percent_uts in ['85%uts']:
                                        applied_stress = 0.85 * typei_uts
                                    elif percent_uts in ['75%uts']:
                                        applied_stress = 0.75 * typei_uts
                                    else:
                                        applied_stress = 0.65 * typei_uts
                                    # calculate the maximum number of cycles and applied stress for fatigue data
                                    max_cycles = data['Count'].max()
                    for specimen_type in ['d3039']:
                        for frequency in ['0.25hz']:
                            for layer_thickness in ['0.3302']:
                                for infill in ['solid']:
                                    typei_uts = 25.37 #MPa
                                    if percent_uts in ['95%uts']:
                                        applied_stress = 0.95 * typei_uts
                                    elif percent_uts in ['85%uts']:
                                        applied_stress = 0.85 * typei_uts
                                    elif percent_uts in ['75%uts']:
                                        applied_stress = 0.75 * typei_uts
                                    else:
                                        applied_stress = 0.65 * typei_uts
                                    # calculate the maximum number of cycles and applied stress for fatigue data
                                    max_cycles = data['Count'].max()
                    for specimen_type in ['d3039']:
                        for frequency in ['0.25hz']:
                            for layer_thickness in ['0.254']:
                                for infill in ['hd']:
                                    typei_uts = 23.55 #MPa
                                    if percent_uts in ['95%uts']:
                                        applied_stress = 0.95 * typei_uts
                                    elif percent_uts in ['85%uts']:
                                        applied_stress = 0.85 * typei_uts
                                    elif percent_uts in ['75%uts']:
                                        applied_stress = 0.75 * typei_uts
                                    else:
                                        applied_stress = 0.65 * typei_uts
                                    # calculate the maximum number of cycles and applied stress for fatigue data'''
                                    max_cycles = data['Count'].max()
                    for specimen_type in ['d3039']:
                        for frequency in ['0.25hz']:
                            for layer_thickness in ['0.3302']:
                                for infill in ['hd']:
                                    typei_uts = 21.25 #MPa
                                    if percent_uts in ['95%uts']:
                                        applied_stress = 0.95 * typei_uts
                                    elif percent_uts in ['85%uts']:
                                        applied_stress = 0.85 * typei_uts
                                    elif percent_uts in ['75%uts']:
                                        applied_stress = 0.75 * typei_uts
                                    else:
                                        applied_stress = 0.65 * typei_uts
                                    # calculate the maximum number of cycles and applied stress for fatigue data'''
                                    max_cycles = data['Count'].max()
                    Fatigue = Fatigue + file + ' ' + str(applied_stress) + ' ' + str(max_cycles) + '\n'

            True

print(Fatigue)
a1 = open('output', 'w')
a1.writelines(Fatigue)
#    data.to_excel('data/'+file_name+'.xlsx')