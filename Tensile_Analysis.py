import pandas as pd
import re
import matplotlib.pyplot as plt
import os
import seaborn as sns
from scipy import stats
import difflib


'''set cross-sectional area based on specimen type'''
area = 41.6 #mm^2
'''gauge length'''
g_len = 50 #mm

'''get excel files with raw data, stress, strain for plotting and vlookup use'''
file = 'data/low_high_4545_typei_monotonic_r06.xls'

'''get file name to write output file'''
file_name = os.path.splitext(file)[0]
file_name = os.path.basename(file_name)
print(file_name)

'''create list of column titles'''
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

'''plot Stress vs. Strain'''
data.plot(y='Stress', x='Strain')

'''plotting trendline for corrected load vs Extension'''
sns.lmplot(y='Stress', x='Strain', data = data,fit_reg=False)

'''get coeffs of linear fit'''
slope, intercept, r_value, p_value, std_err = stats.linregress(data.iloc[100:600]['Strain'], data.iloc[100:600]['Stress'])
print('The Elastic Modulus is {}'.format(slope))
print('The unshifted y-intercept is {}'.format(intercept))
print('The R-Value is {}'.format(r_value))
print('The P-Value is {}'.format(p_value))
print('The Standard Error is {}'.format(std_err))

'''graph the linear fit used to determine the elastic modulus of the raw data'''
y_plot = slope* (data[0:600]['Strain']) + intercept

plt.plot(data[0:600]['Strain'], y_plot, color='r')

'''Toe Compensated Strain that shifts the Stress/strain curve to the left - set y_plot = 0 and solve for x = intercept/slope'''
TC_offset =-intercept/slope
data['TCStrain']=data['Strain']-TC_offset
print('The Toe Compensation Offset is {} mm/mm'.format(TC_offset))

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
print(tcstressdata.iloc[400:500])

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
print(tccurvedata.head())

tccurvedata.to_excel('data/'+file_name+'_tccurve.xls')

'''plot TC Stress vs. TC Strain'''
tccurvedata.plot(y='TCStress', x='TCStrain')

'''now let's plot the TC Stress v. TC Strain linear fit'''
sns.lmplot(y='TCStress', x='TCStrain', data=tccurvedata, fit_reg=False)

'''get coeffs of linear fit of the toe compensated elastic region'''
tc_slope, tc_intercept, tc_r_value, tc_p_value, tc_std_err = stats.linregress(tccurvedata.iloc[100:800]['TCStrain'], tccurvedata.iloc[100:800]['TCStress'])
print('The Toe Compensated Elastic Modulus is {}'.format(tc_slope))
print('The Toe Compensated y-intercept is {}'.format(tc_intercept))
print('The R-Value of the linear regression fit is {}'.format(tc_r_value))
print('The P-Value is {}'.format(tc_p_value))
print('The Standard Error of the fit is {}'.format(tc_std_err))

'''graph the linear fit used to determine the elastic modulus of the TC curve'''

tc_y_plot = tc_slope* (tccurvedata.iloc[0:800]['TCStrain']) + tc_intercept

plt.plot(tccurvedata.iloc[0:800]['TCStrain'], tc_y_plot, color='r')

plt.show()

