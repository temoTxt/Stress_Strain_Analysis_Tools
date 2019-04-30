import pandas as pd
import re
import csv
import matplotlib.pyplot as plt
import os
import openpyxl
from openpyxl import Workbook, load_workbook

Tensile = 'File Name \t Printer \t UTS (MPa) \t Stress at Failure (MPa) \t Strain at Failure (mm/mm) \n'
'''get file locations of the raw .dat file for uprint v. dimension testing'''
for i in range(0, 4):
    layer_infill = ['0.254_solid_', '0.3302_solid_', '0.254_hd_', '0.3302_hd_']
    file_front = 'data/' + str(layer_infill[i])
    # print(file_front)
    for j in range(0,2):
        printer = ['uprint', 'dimension']
        file_middle = file_front + str(printer[j]) + '_'
        # print(file_middle)
        for k in range(0,2):
            type = ['typei', 'typeiv']
            file_back = file_middle + str(type[k])
            for n in range(0, 2):
                raster = ['_4545_', '_090_']
                file_last = file_back + str(raster[n]) + 'r('
                for replicates in range(1, 11):
                    file = file_last + str(replicates) + ').dat'
                    # print(file)
                    split_filename = file.split('_')
                    specimen_type = split_filename[3]
                    printer = split_filename[2]
                    layer = split_filename[0]
                    split_layer = layer.split('/')
                    layer_thickness = split_layer[1]
                    infill = split_filename[1]

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
                    # print('The '+str(specimen_type)+' cross-sectional area is', area, ' mm2')
                    # print('The '+str(specimen_type)+' gage length is', g_len, ' mm')
                    '''get file name to write output file'''
                    file_name = os.path.splitext(file)[0]
                    file_name = os.path.basename(file_name)
                    # print(file_name)

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

                            col_name = ['Displacement', 'Force', 'Time']

                            '''create pandas dataframe with the cleaned data'''
                            data = pd.DataFrame(clean_data, columns=col_name)
                            # print(data.head())

                            '''change the data from being a string to a float datatype'''
                            data = data.astype(float)

                            '''Stress calculation'''
                            data['Stress'] = data['Force'] / area

                            '''Normalize the Displacement'''
                            data['NormalDisplacement'] = data['Displacement']-data.iloc[0]['Displacement']

                            '''Strain Calculation'''
                            data['Strain'] = data['NormalDisplacement'] / g_len
                            # print(data['Strain'])
                            # print(data['Stress'])

                            '''calculating UTS, stress at break, strain at break, and strain at UTS'''
                            '''Calculate UTS'''
                            max_stress = round(data['Stress'].max(), 2)
                            # print('The UTS for ', '"', file_name, '" is ', max_stress,' MPa.')
                            '''delete all the negative values in the data for strain and stress'''
                            data['Stress_nonneg'] = data['Stress'][data['Stress'] >= 0]
                            data['Strain_nonneg'] = data['Strain'][data['Strain'] >= 0]
                            '''Drop all the NaN values'''
                            data = data.dropna(axis='rows', how='any')
                            # print(data['Stress_nonneg'])
                            '''Find the Strain at break'''
                            strain_break = round(data['Strain_nonneg'].max(), 4)
                            stress_break = round(data['Stress_nonneg'].iloc[-2], 2)
                            # print('The strain at break for "', file_name, '" is ', strain_break, ' mm/mm.')
                            '''Take the difference with each row in Stress_nonneg'''
                            # print('The stress at break for "', file_name, '" is ', stress_break, ' MPa.')
                            Tensile = Tensile + str(file_name) +'\t' + str(printer) + '\t' + str(max_stress) + '\t' + str(stress_break) + '\t' + str(strain_break) + '\n'
                            #data.to_excel('data/processed_data_files/fatigue/' + file_name + '.xlsx')
                    True

print(Tensile)
tensile_data = open('data/tensile_output', 'r+')
tensile_data.writelines(Tensile)
