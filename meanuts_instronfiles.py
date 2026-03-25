import pandas as pd
import re
import matplotlib.pyplot as pyplt
import os
import seaborn as sns
from scipy import stats

Tensile = 'File Name \t Dose (MGy) \t UTS (MPa) \t Maximum Load (N) \t Area (mm2) \t Elastic Modulus (MPa) \t ' \
          'Yield Stress (MPa) \t Strain Hardening Ratio \t Modulus of Toughness (MPa) \n'
'''get file locations of the raw .csv file for '''
for i in range(0, 5):
    dose = ['Pristine_','0.1MGy_', '0.2MGy_', '0.5MGy_', '1.0MGy_']
    file_front = 'data/' + str(dose[i])

    for j in range(0,2):
        thickness = ['5layer_1.23.20.Specimen_RawData_', '13layer_1.23.20.Specimen_RawData_']
        file_middle = file_front + str(thickness[j])

        for replicates in range(1, 4):
            file = file_middle + str(replicates) + '.dat'

            split_filename = file.split('_')
            specimen_type = split_filename[1]
            dose_applied = split_filename[0]
            filename = file.split('/')
            fig = filename[1]
            fig_filename = fig.split('.dat')
            filename_fig = fig_filename[0]
            g_len = 25  # mm
            if specimen_type in ['5layer']:
                '''5 layer cross-sectional area'''
                area = 6*1.36  # cm^2

            else:
                '''13 layer cross section area'''
                area = 6*3.3302 # cm^2


                # print('The '+str(specimen_type)+' cross-sectional area is', area, ' mm2')
                # print('The '+str(specimen_type)+' gage length is', g_len, ' mm')
                '''get file name to write output file'''
                file_name = os.path.splitext(file)[0]
                file_name = os.path.basename(file_name)


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

                    col_name = ['Time', 'Extension', 'Load']

                    '''create pandas dataframe with the cleaned data'''
                    data = pd.DataFrame(clean_data, columns=col_name)
                    #print(data.head())

                    '''change the data from being a string to a float datatype'''
                    data = data.astype(float)
                    data['zeroedload']=data['Load']-data.iloc[0]['Load']
                    '''Stress calculation'''
                    data['Stress'] = data['zeroedload'] / area

                    '''Normalize the Displacement'''
                    data['NormalDisplacement'] = data['Extension']-data.iloc[0]['Extension']

                    '''Strain Calculation'''
                    data['Strain'] = data['NormalDisplacement'] / g_len
                    # print(data['Strain'])
                    # print(data['Stress'])
                    #print(data.head())
                    '''calculating UTS, stress at break, strain at break, and strain at UTS'''
                    '''Calculate UTS'''
                    max_load = round(data['zeroedload'].max(),2)
                    max_stress = round(data['Stress'].max(), 2)
                    #print('The UTS for ', '"', file_name, '" is ', max_stress,' MPa with a maximum load of ',max_load,'.')
                    '''delete all the negative values in the data for strain and stress'''
                    #data['Stress_nonneg'] = data['Stress'][data['Stress'] >= 0]
                    #data['Strain_nonneg'] = data['Strain'][data['Strain'] >= 0]
                    '''Drop all the NaN values'''
                    #data = data.dropna(axis='rows', how='any')
                    # print(data['Stress_nonneg'])
                    '''Find the Strain at break'''
                    #strain_break = round(data['Strain_nonneg'].max(), 4)
                    #stress_break = round(data['Stress_nonneg'].iloc[-2], 2)
 #                   # print('The strain at break for "', file_name, '" is ', strain_break, ' mm/mm.')
 #                   '''Take the difference with each row in Stress_nonneg'''
 #                   # print('The stress at break for "', file_name, '" is ', stress_break, ' MPa.')
 #                   Tensile = Tensile + str(file_name) +'\t' + str(max_stress) + '\n'
 #                   #data.to_excel('data/processed_data_files/fatigue/' + file_name + '.xlsx')

                    '''plotting trendline for corrected load vs Extension'''
                    sns.lmplot(y='Stress', x='Strain', data=data, fit_reg=False)

                    '''get coeffs of linear fit'''
                    slope, intercept, r_value, p_value, std_err = stats.linregress(data.iloc[20:50]['Strain'],
                                                                                   data.iloc[20:50]['Stress'])
                    # print('The Elastic Modulus is {}'.format(slope))
                    # print('The unshifted y-intercept is {}'.format(intercept))
                    # print('The R-Value is {}'.format(r_value))
                    # print('The P-Value is {}'.format(p_value))
                    # print('The Standard Error is {}'.format(std_err))
                    pyplt.clf()
                    pyplt.close('all')
                    '''graph the linear fit used to determine the elastic modulus of the raw data'''
                    y_plot = slope * (data[0:80]['Strain']) + intercept
                    #calculate the 0.2% offset y-intercept point

                    #create points for 0.2% offset line for intersection
                    data['offset_strain'] = data['Strain'] + 0.002
                    offset_yintercept = -(data.iloc[0]['offset_strain']) * slope
                    data['offset_stress'] = slope * (data.iloc[0:800]['offset_strain']) \
                                                   + offset_yintercept
                    pyplt.plot(data['Strain'], data['Stress'], color='b')
                    pyplt.plot(data[0:80]['Strain'], y_plot, color='r')
                    pyplt.plot(data[0:150]['offset_strain'], data[0:150]['offset_stress'], color = 'g')
                    pyplt.xlabel('Strain (mm/mm)')
                    pyplt.ylabel('Stress (MPa)')
                    pyplt.savefig('data/processed_data_files/tensile/' + filename_fig + '.png')
                    pyplt.close()


                    '''create vlookup dataframe'''
                    vl_col_name = ['Strain', 'Stress']
                    vlookup = pd.DataFrame(data, columns=vl_col_name)

                    '''change the data from being a string to a float datatype'''
                    vlookup = vlookup.astype(float)


                    # print(data.head())
                    '''sorting required so we don't get an error when we merge_asof'''
                    data = data.sort_values('offset_strain')
                    vlookup = vlookup.sort_values('Strain')

                    '''performs a vlookup to match the raw data strain to the TCStrain and return the rawdata stress 
                    to the offset Stress column'''
                    offsetdata = pd.merge_asof(data, vlookup, left_on='offset_strain', right_on='Strain',
                                               direction='nearest')
                    # print(offsetdata.iloc[400:405])
                    offset_col_name = ['offset_strain', 'offset_stress', 'Strain_x', 'Stress_x', 'error']
                    offset = pd.DataFrame(offsetdata, columns=offset_col_name)
                    offset = offset.astype(float)
                    # offset = offset.dropna(axis='rows', how='any')
                    # print(offset.head())
                    offset['error'] = (offset['offset_stress'] - offset['Stress_x']) / offset['Stress_x']
                    offset['error'] = offset['error'].abs()
                    offset = offset.iloc[3:]
                    yield_stress = round(offset.iloc[offset['error'].idxmin()]['Stress_x'], 2)
                    yield_strain = round(offset.iloc[offset['error'].idxmin()]['Strain_x'], 4)
                    '''calculate tensile data parameters from determined values'''
                    strain_hardening_ratio = round(max_stress/yield_stress, 2)
                    modulus_toughness = round(((yield_stress+max_stress)*yield_strain/2)-
                     ((((yield_stress+max_stress)/2)**2)/(2*slope)), 2)

                    '''place all tensile parameters in a table'''
                    Tensile = Tensile + str(file) + '\t' + str(dose_applied) + '\t' + str(max_stress) + '\t' + \
                             str(max_load) + '\t' + str(area) + '\t' + str(round(slope,2)) + '\t' + str(yield_stress)+ \
                              '\t' +str(strain_hardening_ratio)+ '\t'+str(modulus_toughness)+'\n'
                    offset.to_excel('data/processed_data_files/tensile/' + filename_fig + '.xlsx')
            True

print(Tensile)
tensile_data = open('data/output', 'r+')
tensile_data.writelines(Tensile)
