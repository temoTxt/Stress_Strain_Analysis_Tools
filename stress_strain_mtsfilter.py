import pandas as pd
import re
import matplotlib.pyplot as pyplt
import os
import seaborn as sns
from scipy import stats, signal
import numpy as np

Tensile = 'File Name \t Dose (MGy) \t UTS (MPa) \t Elastic Modulus (MPa) \t 0.2% Offset Yield Stress \t ' \
          '0.2% Offset Yield Strain \t Strain Hardening Ratio \t Modulus of Toughness \n'
'''get file locations of the raw .dat file'''
for i in range(0, 3):
    thickness = ['3.3302_', '1.27_', '0.2540_']
    file_front = 'data/' + str(thickness[i])
    # print(file_front)
    for j in range(0, 7):
        dose = ['0mgy', '0.1mgy', '0.2mgy', '0.3mgy', '0.5mgy', '0.6mgy', '1.0mgy']
        file_middle = file_front + str(dose[j]) + '_r('
        # print(file_middle)
        for replicates in range(1, 13):
            file = file_middle + str(replicates) + ').dat'
            # print(file)
            split_filename = file.split('_')
            dose = split_filename[1]
            layer = split_filename[0]
            split_layer = layer.split('/')
            layer_thickness = split_layer[1]

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
                    #index is time.
                    #data = data.set_index('Time')
                    #print(data.head())

                    '''change the data from being a string to a float datatype'''
                    data = data.astype(float)

                    '''gauge length'''
                    g_len = 25  # mm
                    # select the correct cross sectional area for specimen based on thickness
                    if layer_thickness in ['3.3302']:
                        area = 6 * 3.3302  # cm^2

                    elif layer_thickness in ['1.27']:
                        area = 6 * 1.27  # cm^2
                        '''gauge length'''

                    elif layer_thickness in ['0.2540']:
                        area = 6 * 0.2540  # cm^2

                    else:
                        area = 6 * 3.3  # cm^2

                    '''downsample the raw data by slicing created aliasing so let's run a filter'''
                    #data = data[::20]

                    fig, ax = pyplt.subplots()
                    ax.plot(data['Displacement'], data['Force'], label="Original")
                    '''calculating the running average using different window sizes'''
                    window_lst = [3, 6, 10, 16, 22, 35]
                    y_avg = np.zeros((len(window_lst), len(data['Displacement'])))
                    for i, window in enumerate(window_lst):
                        avg_mask = np.ones(window) / window
                        y_avg[i, :] = np.convolve(data['Force'], avg_mask, 'same')
                        # Plot each running average with an offset of 50
                        # in order to be able to distinguish them
                        ax.plot(data['Displacement'], y_avg[i, :] + (i + 1) * 50, label=window)
                    # Add legend to plot
                    ax.legend()
                    # add labels to the axes
                    pyplt.xlabel('Un-Normalized Displacement (mm)')
                    pyplt.ylabel('Force (N)')
                    #pyplt.show()
                    pyplt.clf()

                    # '''Trying a guassian window for data smoothing'''
                    # gaussian_func = lambda x, sigma: 1 / np.sqrt(2 * np.pi * sigma ** 2) * np.exp(
                    #     -(x ** 2) / (2 * sigma ** 2))
                    # fig, ax = pyplt.subplots()
                    # # Compute moving averages using different window sizes
                    # sigma_lst = [1, 2, 3, 5, 8, 10]
                    # y_gau = np.zeros((len(sigma_lst), len(data['Displacement'])))
                    # for j, sigma in enumerate(sigma_lst):
                    #     gau_x = np.linspace(-2.7 * sigma, 2.7 * sigma, 6 * sigma)
                    #     gau_mask = gaussian_func(gau_x, sigma)
                    #     y_gau[j, :] = np.convolve(data['Force'], gau_mask, 'same')
                    #     ax.plot(data['Displacement'], y_gau[j, :] + (j + 1) * 50,
                    #             label=r"$\sigma = {}$, $points = {}$".format(sigma, len(gau_x)))
                    # # Add legend to plot
                    # ax.legend(loc='upper left')
                    # #pyplt.show()
                    # pyplt.savefig('data/processed_data_files/tensile/' + file_name + '_gau.png')

                    '''add a new column for the smoothed data y_avg from the window 35'''
                    data.insert(3,'Smoothed_Force',y_avg[5])
                    #print(data.head())

                    '''Apply the smoothed force data for the rest of the analysis'''
                    '''Stress calculation'''
                    data['Stress'] = data['Smoothed_Force'] / area
                    '''Calculate UTS'''
                    max_stress = round(data['Stress'].max(), 2)

                    '''Normalize the Displacement'''
                    data['NormalDisplacement'] = data['Displacement']-data.iloc[0]['Displacement']

                    '''Strain Calculation'''
                    data['Strain'] = data['NormalDisplacement'] / g_len
                    #print(data['Strain'])
                    #print(data['Stress'])

                    '''plot Stress vs. Strain'''
                    #data.plot(y='Stress', x='Strain')

                    '''plotting trendline for corrected load vs Extension'''
                    sns.lmplot(y='Stress', x='Strain', data=data, fit_reg=False)

                    '''get coeffs of linear fit'''
                    slope, intercept, r_value, p_value, std_err = stats.linregress(data.iloc[100:600]['Strain'],
                                                                                   data.iloc[100:600]['Stress'])
                    #print('The Elastic Modulus is {}'.format(slope))
                    #print('The unshifted y-intercept is {}'.format(intercept))
                    #print('The R-Value is {}'.format(r_value))
                    #print('The P-Value is {}'.format(p_value))
                    #print('The Standard Error is {}'.format(std_err))
                    pyplt.clf()
                    pyplt.close('all')
                    '''graph the linear fit used to determine the elastic modulus of the raw data'''
                    y_plot = slope * (data[0:600]['Strain']) + intercept

                    #plt.plot(data[0:600]['Strain'], y_plot, color='r')

                    '''Toe Compensated Strain that shifts the Stress/strain curve to the left - set y_plot = 0 and 
                    solve for x = intercept/slope'''
                    TC_offset = -intercept/slope
                    data['TCStrain'] = data['Strain']-TC_offset
                    #print('The Toe Compensation Offset is {} mm/mm'.format(TC_offset))

                    '''Shift the TCStrain_nonneg values up, removing the NaN values without loosing any of the other 
                    data - this DOES NOT remove rows'''
                    data = data.apply(lambda x: pd.Series(x.dropna().values))
                    #print(tcdata.head())

                    '''create vlookup dataframe'''
                    vl_col_name = ['Strain', 'Stress']
                    vlookup = pd.DataFrame(data, columns=vl_col_name)

                    '''change the data from being a string to a float datatype'''
                    vlookup = vlookup.astype(float)

                    '''sorting required so we don't get an error when we merge_asof'''
                    data = data.sort_values('TCStrain')
                    vlookup = vlookup.sort_values('Strain')

                    '''performs a vlookup to match the raw data strain to the TCStrain and return the rawdata stress to 
                    the TCStress column'''
                    tcstressdata = pd.merge_asof(data, vlookup, left_on='TCStrain', right_on='Strain',
                                                 direction='nearest')
                    # print(tcstressdata.iloc[400:500])

                    '''Remove negative values in Strain_y column.  This will create NaN values that we will cleanup 
                    in the next step'''
                    tcstressdata['TCStrain_nonneg'] = tcstressdata['Strain_y'][tcstressdata['Strain_y'] >= 0]

                    '''Drop the rows with NaN values at the beginning.  NaN values should only be in the TCStrain_
                    nonneg column'''
                    tcstressdata = tcstressdata.dropna(axis='rows', how='any')

                    tcstress_col_name = ['TCStrain', 'Stress_x']
                    tccurvedata = pd.DataFrame(tcstressdata, columns=tcstress_col_name)

                    '''change the data from being a string to a float datatype'''
                    tccurvedata = tccurvedata.astype(float)

                    '''rename tccurvedata column names'''
                    tccurvedata.columns = ['TCStrain', 'TCStress']
                    #print(tccurvedata.head())

                    # tccurvedata.to_excel('data/'+file_name+'_tccurve.xls')

                    '''Remove negative values in Strain_y column.  Thiw will create NaN values that we will cleanup 
                    in the next step'''
                    tccurvedata['TCStress'] = tccurvedata['TCStress'][tccurvedata['TCStress'] >= 0]

                    '''Drop the rows with NaN values at the beginning.  NaN values should only be in the TCStrain_
                    nonneg column'''
                    tccurvedata = tccurvedata.dropna(axis='rows', how='any')

                    '''plot TC Stress vs. TC Strain-the blue line'''
                    #tccurvedata.plot(y='TCStress', x='TCStrain', kind = 'line')
                    #plt.plot(tccurvedata['TCStrain'],tccurvedata['TCStress'])

                    '''now let's plot the TC Stress v. TC Strain linear fit'''
                    sns.lmplot(y='TCStress', x='TCStrain', data=tccurvedata, fit_reg=False)


                    '''get coeffs of linear fit of the toe compensated elastic region'''
                    tc_slope, tc_intercept, tc_r_value, tc_p_value, \
                    tc_std_err = stats.linregress(tccurvedata.iloc[100:800]['TCStrain'],
                                                  tccurvedata.iloc[100:800]['TCStress'])
                    #print('The Toe Compensated Elastic Modulus is {}'.format(tc_slope))
                    #print('The Toe Compensated y-intercept is {}'.format(tc_intercept))
                    #print('The R-Value of the linear regression fit is {}'.format(tc_r_value))
                    #print('The P-Value is {}'.format(tc_p_value))
                    #print('The Standard Error of the fit is {}'.format(tc_std_err))
                    '''graph the linear fit used to determine the elastic modulus of the TC curve'''
                    elastic = round(tc_slope, 1)
                    tc_y_plot = tc_slope * (tccurvedata.iloc[0:800]['TCStrain']) + tc_intercept
                    offset_yintercept = -(tccurvedata.iloc[0]['TCStrain']+0.002)/tc_slope
                    #print(offset_yintercept)

                    tccurvedata['offset_strain'] = tccurvedata['TCStrain'] + 0.002
                    tccurvedata['offset_stress'] = tc_slope*(tccurvedata.iloc[0:1800]['offset_strain']) \
                                                   + offset_yintercept
                    '''clear all the sns plots from the plot function'''
                    pyplt.clf()

                    '''stress v. strain curve'''
                    pyplt.plot(tccurvedata['TCStrain'], tccurvedata['TCStress'])
                    pyplt.xlabel('Strain (mm/mm)')
                    pyplt.ylabel('Stress (MPa)')
                    #pyplt.show()
                    '''elastic modulus line'''
                    #pyplt.plot(tccurvedata.iloc[0:800]['TCStrain'], tc_y_plot, color='r')
                    #pyplt.show()
                    '''plotting the offset line'''
                    #pyplt.plot(tccurvedata.iloc[0:1800]['offset_strain'], tccurvedata.iloc[0:1800]['offset_stress'],
                    #         color='y')
                    #pyplt.show()
                    #pyplt.savefig('data/processed_data_files/tensile/' + file_name + '.png')

                    #plt.show()

                    '''sorting required so we don't get an error when we merge_asof'''
                    tccurvedata = tccurvedata.sort_values('offset_strain')
                    vlookup = vlookup.sort_values('Strain')

                    '''performs a vlookup to match the raw data strain to the TCStrain and return the rawdata stress 
                    to the offset Stress column'''
                    offsetdata = pd.merge_asof(tccurvedata, vlookup, left_on='offset_strain', right_on='Strain',
                                                 direction='nearest')
                    #print(offsetdata.iloc[400:405])
                    offset_col_name = ['offset_strain', 'offset_stress', 'Strain', 'Stress', 'TCStrain']
                    offset = pd.DataFrame(offsetdata, columns=offset_col_name)
                    offset = offset.astype(float)
                    offset['error'] = (offset['offset_stress']-offset['Stress'])/offset['Stress']
                    offset['error'] = offset['error'].abs()
                    #print(offset.iloc[400:405])
                    yield_stress = round(offset.iloc[offset['error'].idxmin()]['Stress'], 2)
                    yield_strain = round(offset.iloc[offset['error'].idxmin()]['TCStrain'], 4)
                    '''calculate tensile data parameters from determined values'''
                    strain_hardening_ratio = round(max_stress/yield_stress, 2)
                    modulus_toughness = round(((yield_stress+max_stress)*yield_strain/2)-
                                              ((((yield_stress+max_stress)/2)**2)/(2*elastic)), 2)
                    '''place all tensile parameters in a table'''
                    Tensile = Tensile + str(file_name) + '\t' + str(dose) + '\t' + str(max_stress) + '\t' + \
                              str(elastic) + '\t' + str(yield_stress) + '\t' + str(yield_strain) + '\t' + \
                              str(strain_hardening_ratio) + '\t' + str(modulus_toughness) + '\n'
                    #offsetdata.to_excel('data/processed_data_files/tensile/' + file_name + '.xlsx')
            True

print(Tensile)
#tensile_data = open('data/1.27_0MGy_elastic_output.txt', 'r+')
#tensile_data.writelines(Tensile)
