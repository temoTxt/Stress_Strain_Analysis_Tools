import pandas as pd
import re
import matplotlib.pyplot as plt
import os
import seaborn as sns
from scipy import stats


'''set cross-sectional area based on specimen type'''
area = 41.6 #mm^2
'''gauge length'''
g_len = 50 #mm

'''get excel files with raw data, stress, strain for plotting and vlookup use'''
file = 'data/low_high_4545_typei_monotonic_r06.xls'
file_vlookup = 'data/low_high_4545_typei_monotonic_r06_vlookup.xls'

'''get file name to write output file'''
file_name = os.path.splitext(file)[0]
file_name = os.path.basename(file_name)
print(file_name)

'''open file as a giant text blob'''
#text = open(file, 'r+')

'''seperate blob into lines of text'''
#lines = text.readlines()

'''create list object to put in only numerical data'''
#clean_data = []

'''go line by line to scrub header data'''
#for line in lines:

#    '''convert all \t to an actual tab in the data'''
#    line = line.replace('\t', ',')
    #print(line)

#    '''strip out the \n at the end of each line'''
#    line = line.rstrip()

#    '''check to see if there are any letters in the string. If there are not it must be a data line'''
#    if re.search('[a-zA-Z]', line) == None:

#        '''if there is actually values in the line then we add it to our cleaned data list object'''
#       if len(line) > 4:

#            '''split the line into multiple elements using the comma as the anchor point'''
#            line = line.split(',')

#            '''add this line to the list object for ingest into Pandas'''
#            clean_data.append(line)

#'''create list of column titles'''
#col_name = ['Force', 'Displacement', 'Time', 'Count']
col_name = ['Strain', 'Stress','TCStrain','TCStrain_nonneg']

'''create pandas dataframe with the cleaned data'''
data = pd.read_excel(file)
print(data.head())

'''change the data from being a string to a float datatype'''
data = data.astype(float)

'''finding maximum of untrimmed and unsmoothed data'''
maxload = data['Force'].max()

'''displaying maximum of untrimmed and unsmoothed data'''
print('The Max Load is {} N'.format(maxload))

'''finding maximum stresss from untrimmed and unsmoothed data'''
strength = maxload / area

'''displaying maximum stress from untrimmed and unsmoothed data'''
print('The Max Stress is {} MPa'.format(strength))


'''print out specfic coloumns of the dataframe'''
#print(data['Force'])
#print(data['Displacement'])
#print(data['Time'])
#print(data['Count'])

'''try to take out the data after the specimen has broken'''
#data = data[0:-75]

#data.to_excel(file_name+'.xls')
#data['difference'] = data['Stress'].diff()

'''trim front part of data'''
#data = data[100:-1]

'''defining windowlength'''
#windowlength = 50

'''smoothing data with a window of windowlength'''
#data['smooth'] = data['difference'].rolling(windowlength).mean()

'''finding initial maximum of trimmed and smoothed data'''
#minrange = data['smooth'].idxmax()

'''corrected minrange value based on windowlength'''
#correctedminrange = minrange - (3 * windowlength)

'''taking the difference of the difference'''
#data['differencetoo'] = data['difference'].diff()

'''plot differencetoo vs Extension'''
#data.plot(y='differencetoo', x='Displacement')

'''smoothing differencetoo data with a window of 1000'''
#data['smoothtoo'] = data['differencetoo'].rolling(1000).mean()

'''plot smoothtoo vs Extension'''
#data.plot(y='smoothtoo', x='Displacement')

'''finding initial minimum of trimmed and smoothedtoo data'''
#maxrange = data['smoothtoo'].idxmin()

'''plot Slope'''
#data.plot(y='difference', x='Displacement')

'''plot Stress vs. Strain'''
#data.plot(y='Force', x='Displacement')

'''plot Smooth vs. Time'''
#data.plot(y='smooth', x='Extension')

'''plot Stress vs. Strain'''
#data.plot(y='Force', x='Extension')

'''defining ax variable to be corrrected midrange vs maxrange'''
#ax = data.iloc[50:80].plot(y='Force', x='Displacement')


'''plotting trendline for corrected load vs Extension'''
sns.lmplot(y='Stress', x='Strain', data = data,fit_reg=False)


# get coeffs of linear fit
slope, intercept, r_value, p_value, std_err = stats.linregress(data.iloc[100:600]['Strain'], data.iloc[100:600]['Stress'])
print(data.iloc[100:600]['Strain'])
#print(slope)
print('The Elastic Modulus is {}'.format(slope))
#print(intercept)
print('The unshifted y-intercept is {}'.format(intercept))
#print(r_value)
print('The R-Value is {}'.format(r_value))
#print(p_value)
print('The P-Value is {}'.format(p_value))
#print(std_err)
print('The Standard Error is {}'.format(std_err))


'''plotting trendline for raw data as stress v. strain'''
#sns.lmplot(y='Stress', x='Strain', data = data,fit_reg=False)

# plot legend
#ax.legend()

y_plot = slope* (data.iloc[0:600]['Strain']) + intercept

plt.plot(data.iloc[0:600]['Strain'], y_plot, color='r')

plt.show()

'''Toe Compensated Strain that shifts the Stress/strain curve to the left - set y_plot = 0 and solve for x = intercept/slope'''
TC_offset =-intercept/slope
data['TCStrain']=data['Strain']-TC_offset
print('The Toe Compensation Offset is {} mm/mm'.format(TC_offset))

'''Remove negative values in TCStrain column TCStrain_nonneg'''
data['TCStrain_nonneg'] = data['TCStrain'][data['TCStrain']>=0]
print(data['TCStrain_nonneg'])

'''Export Stress, Strain, and TCStrain_nonneg columns into new dataframe'''
tc_col_name=['TCStrain', 'TCStrain_nonneg']
tcdata = pd.DataFrame(data, columns=tc_col_name)

'''change the data from being a string to a float datatype'''
tcdata = tcdata.astype(float)
print(tcdata.head())

'''Shift the TCStrain_nonneg values up, removing the NaN values without loosing any of the other data - this DOES NOT remove rows'''

tcdata = tcdata.apply(lambda x: pd.Series(x.dropna().values))
print(tcdata.head())

'''rename tcdata column names'''
tcdata.columns=['TCStrain', 'Strain']
print(tcdata.head())

'''Read the vlookup excel file created from dat_file_cleaning.py so we can find the TC Stress values'''
vlookup = pd.read_excel(file_vlookup)
print(vlookup.head())

'''change the data from being a string to a float datatype'''
vlookup = vlookup.astype(float)

'''everything works up to this point'''

'''performs a vlookup to match the raw data strain to the TCStrain_nonneg and return the rawdata stress to the TCStress column'''
#tcstressdata = pd.merge_asof(vlookup, tcdata, left_on='Strain', right_on='TCStrain_nonneg', direction='nearest')
#index=vlookup['Strain']
#new_index=tcdata['TCStrain_nonneg']
tcstressdata = vlookup.reindex_like(tcdata)
print(tcstressdata.head())


