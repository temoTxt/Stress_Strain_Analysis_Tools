import pandas as pd
import re
import matplotlib.pyplot as plt
import os
import seaborn as sns
from scipy import stats
import difflib

Tensile = 'File Name \t Printer \t Elastic Modulus (MPa) \n'
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
                            '''Calculate UTS'''
                            max_stress = round(data['Stress'].max(), 2)
                            
                            '''Normalize the Displacement'''
                            data['NormalDisplacement'] = data['Displacement']-data.iloc[0]['Displacement']

                            '''Strain Calculation'''
                            data['Strain'] = data['NormalDisplacement'] / g_len
                            # print(data['Strain'])
                            # print(data['Stress'])

                            '''plot Stress vs. Strain'''
                            data.plot(y='Stress', x='Strain')

                            '''plotting trendline for corrected load vs Extension'''
                            fig = sns.lmplot(y='Stress', x='Strain', data=data, fit_reg=False)

                            '''get coeffs of linear fit'''
                            slope, intercept, r_value, p_value, std_err = stats.linregress(data.iloc[100:600]['Strain'], data.iloc[100:600]['Stress'])
                            #print('The Elastic Modulus is {}'.format(slope))
                            #print('The unshifted y-intercept is {}'.format(intercept))
                            #print('The R-Value is {}'.format(r_value))
                            #print('The P-Value is {}'.format(p_value))
                            #print('The Standard Error is {}'.format(std_err))
                            plt.close('all')
                            '''graph the linear fit used to determine the elastic modulus of the raw data'''
                            y_plot = slope * (data[0:600]['Strain']) + intercept

                            #plt.plot(data[0:600]['Strain'], y_plot, color='r')

                            '''Toe Compensated Strain that shifts the Stress/strain curve to the left - set y_plot = 0 and solve for x = intercept/slope'''
                            TC_offset =-intercept/slope
                            data['TCStrain'] = data['Strain']-TC_offset
                            #print('The Toe Compensation Offset is {} mm/mm'.format(TC_offset))

                            '''Shift the TCStrain_nonneg values up, removing the NaN values without loosing any of the other data - this DOES NOT remove rows'''
                            data = data.apply(lambda x: pd.Series(x.dropna().values))
                            #print(tcdata.head())

                            '''create vlookup dataframe'''
                            vl_col_name=['Strain', 'Stress']
                            vlookup = pd.DataFrame(data, columns=vl_col_name)

                            '''change the data from being a string to a float datatype'''
                            vlookup = vlookup.astype(float)

                            '''sorting required so we don't get an error when we merge_asof'''
                            data = data.sort_values('TCStrain')
                            vlookup = vlookup.sort_values('Strain')

                            '''performs a vlookup to match the raw data strain to the TCStrain and return the rawdata stress to the TCStress column'''
                            tcstressdata = pd.merge_asof(data, vlookup, left_on='TCStrain', right_on='Strain', direction='nearest')
                            # print(tcstressdata.iloc[400:500])

                            '''Remove negative values in Strain_y column.  Thiw will create NaN values that we will cleanup in the next step'''
                            tcstressdata['TCStrain_nonneg'] = tcstressdata['Strain_y'][tcstressdata['Strain_y'] >= 0]

                            '''Drop the rows with NaN values at the beginning.  NaN values should only be in the TCStrain_nonneg column'''
                            tcstressdata = tcstressdata.dropna(axis='rows', how='any')

                            tcstress_col_name=['TCStrain', 'Stress_x']
                            tccurvedata = pd.DataFrame(tcstressdata, columns=tcstress_col_name)

                            '''change the data from being a string to a float datatype'''
                            tccurvedata = tccurvedata.astype(float)

                            '''rename tccurvedata column names'''
                            tccurvedata.columns=['TCStrain', 'TCStress']
                            #print(tccurvedata.head())

                            # tccurvedata.to_excel('data/'+file_name+'_tccurve.xls')

                            '''plot TC Stress vs. TC Strain'''
                            tccurvedata.plot(y='TCStress', x='TCStrain')

                            '''now let's plot the TC Stress v. TC Strain linear fit'''
                            fig = sns.lmplot(y='TCStress', x='TCStrain', data=tccurvedata, fit_reg=False)


                            '''get coeffs of linear fit of the toe compensated elastic region'''
                            tc_slope, tc_intercept, tc_r_value, tc_p_value, tc_std_err = stats.linregress(tccurvedata.iloc[100:800]['TCStrain'], tccurvedata.iloc[100:800]['TCStress'])
                            #print('The Toe Compensated Elastic Modulus is {}'.format(tc_slope))
                            #print('The Toe Compensated y-intercept is {}'.format(tc_intercept))
                            #print('The R-Value of the linear regression fit is {}'.format(tc_r_value))
                            #print('The P-Value is {}'.format(tc_p_value))
                            #print('The Standard Error of the fit is {}'.format(tc_std_err))
                            plt.close('all')
                            '''graph the linear fit used to determine the elastic modulus of the TC curve'''

                            tc_y_plot = tc_slope * (tccurvedata.iloc[0:800]['TCStrain']) + tc_intercept

                            #plt.plot(tccurvedata.iloc[0:800]['TCStrain'], tc_y_plot, color='r')

                            #plt.show()
                            Tensile = Tensile + str(file_name) + '\t' + str(printer) + '\t' + str(tc_slope) + '\n'
                            #data.to_excel('data/processed_data_files/fatigue/' + file_name + '.xlsx')
                    True

print(Tensile)
tensile_data = open('data/output', 'r+')
tensile_data.writelines(Tensile)
