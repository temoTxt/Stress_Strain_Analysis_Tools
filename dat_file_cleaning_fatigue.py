import pandas as pd
import re
import csv
import matplotlib.pyplot as plt
import os
import openpyxl
from openpyxl import Workbook, load_workbook

Fatigue = 'File Name \t Max Cycles \n'
'''get file locations of the raw .dat file'''
'''double check that your file names match the naming cadence and fix the code to match your cadence'''
'''or change your cadence to match the code'''
for i in range(0, 4):
    layer_infill = ['0.2540_solid_', '0.3302_solid_', '0.2540_hd_', '0.3302_hd_']
    file_front = 'data/' + str(layer_infill[i])
    for k in range(0, 2):
        type = ['4545', '090']
        file_middle = file_front + str(type[k])
        for j in range(0, 3):
            type = ['_typei_', '_d3039_', '_typeiv_']
            file_middle1 = file_middle + str(type[j])
            for a in range(0, 4):
                uts_percent = ['95%uts', '85%uts', '75%uts', '65%uts']
                file_back = file_middle1 + str(uts_percent[a]) + '_0.25hz_r('
                # change replicate range if you have more than three replicate files
                for replicates in range(1, 4):
                    file = file_back+str(replicates)+').dat'
                    print(file)
                    '''you need to check that the cadence matches the numbering below otherwise the wrong data will be pulled.'''
                    '''use print file to confirm you are getting the file names you think you should'''
                    split_filename = file.split('_')
                    specimen_type = split_filename[3]
                    layer = split_filename[0]
                    percent_uts = split_filename[4]

                    '''get file name to write output file'''
                    file_name = os.path.splitext(file)[0]
                    file_name = os.path.basename(file_name)
                    #print(file_name)

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
                            col_name = ['Force', 'Displacement', 'Time', 'Count']

                            '''create pandas dataframe with the cleaned data'''
                            data = pd.DataFrame(clean_data, columns=col_name)
                            #print(data.head())

                            '''change the data from being a string to a float datatype'''
                            data = data.astype(float)
                            # selects the correct cross-sectional area and gage length for the file/specimen type

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
                                area = 82.5  # cm^2
                                '''D3039 gauge length'''
                                g_len = 180  # mm

                            '''Stress calculation'''
                            data['Stress'] = data['Force'] / area

                            '''Normalize the Displacement'''
                            data['NormalDisplacement'] = data['Displacement']-data.iloc[0]['Displacement']

                            '''Strain Calculation'''
                            data['Strain'] = data['NormalDisplacement'] / g_len
                            #print(data['Strain'])
                            #print(data['Stress'])

                            '''calculating applied stress for each build and each specimen type'''

                            max_cycles = data['Count'].max()
                            Fatigue = Fatigue + str(file_name) + '\t' + str(max_cycles) + '\n'
                            #this part is going to take a while.  like 15 seconds to 30 seconds per excel file.
                            #data.to_excel('data/processed_data_files/fatigue/' + file_name + '.xlsx')
                    True

print(Fatigue)
sncurve_data = open('data/sncurve_output', 'r+')
sncurve_data.writelines(Fatigue)
