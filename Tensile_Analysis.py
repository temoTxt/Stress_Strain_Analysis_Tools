import pandas as pd
import re
import matplotlib.pyplot as plt
import os
import seaborn as sns
from scipy import stats

'''set cross-sectional area'''
area = 19.2 #cm^2
'''gauge length'''
g_len = 25 #mm

'''get file locations of the raw .dat file'''
file = 'data/Specimen_RawData_1.csv'

'''get file name to write output file'''
file_name = os.path.splitext(file)[0]
file_name = os.path.basename(file_name)
print(file_name)

'''open file as a giant text blob'''
text = open(file, 'r+')

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
#col_name = ['Force', 'Displacement', 'Time', 'Count']
col_name = ['Time', 'Extension', 'Load']

'''create pandas dataframe with the cleaned data'''
data = pd.DataFrame(clean_data, columns=col_name)



'''change the data from being a string to a float datatype'''
data = data.astype(float)

'''print out specfic coloumns of the dataframe'''
#print(data['Force'])
#print(data['Displacement'])
#print(data['Time'])
#print(data['Count'])

'''try to take out the data after the specimen has broken'''
data = data[0:-75]

#data.to_excel(file_name+'.xls')
data['difference'] = data['Load'].diff()

'''trim front part of data'''
data = data[100:-1]

'''defining windowlength'''
windowlength = 50

'''smoothing data with a window of windowlength'''
data['smooth'] = data['difference'].rolling(windowlength).mean()

'''finding initial maximum of trimmed and smoothed data'''
minrange = data['smooth'].idxmax()

'''corrected minrange value based on windowlength'''
correctedminrange = minrange - (3 * windowlength)

'''taking the difference of the difference'''
data['differencetoo'] = data['difference'].diff()

'''plot differencetoo vs Extension'''
data.plot(y='differencetoo', x='Extension')

'''smoothing differencetoo data with a window of 1000'''
data['smoothtoo'] = data['differencetoo'].rolling(1000).mean()

'''plot smoothtoo vs Extension'''
data.plot(y='smoothtoo', x='Extension')

'''finding initial minimum of trimmed and smoothedtoo data'''
maxrange = data['smoothtoo'].idxmin()

'''plot Slope'''
#data.plot(y='difference', x='Extension')

'''plot Stress vs. Strain'''
#data.plot(y='Load', x='Extension')

'''plot Smooth vs. Time'''
#data.plot(y='smooth', x='Extension')

'''plot Stress vs. Strain'''
#data.plot(y='Load', x='Extension')

'''defining ax variable to be corrrected midrange vs maxrange'''
ax = data.iloc[correctedminrange:maxrange].plot(y='Load', x='Extension')

'''plotting trendline for corrected load vs Extension'''
sns.lmplot(y='Load', x='Extension', data = data,fit_reg=False)

# get coeffs of linear fit
slope, intercept, r_value, p_value, std_err = stats.linregress(data.iloc[correctedminrange:maxrange]['Extension'], data.iloc[correctedminrange:maxrange]['Load'])

print(slope)
print(intercept)
print(r_value)
print(p_value)
print(std_err)

# plot legend
ax.legend()

y_plot = slope* data.iloc[correctedminrange:maxrange]['Extension'] + intercept

plt.plot(data.iloc[correctedminrange:maxrange]['Extension'], y_plot, color='r')


#data['Extension_corrected'] = data['Extension'] + intercept

#sns.lmplot(y='Load', x='Extension_corrected')

plt.show()
