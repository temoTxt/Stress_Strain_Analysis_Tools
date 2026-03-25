import pandas as pd
import re
import csv
import matplotlib.pyplot as plt
import os

'''set cross-sectional area'''
area = 19.2 #cm^2
'''gauge length'''
g_len = 25 #mm
'''get file locations of the raw .dat file'''
file = 'data/low_high_4545_typei_monotonic_r06.csv'

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
col_name = ['Force', 'Displacement', 'Time']

'''create pandas dataframe with the cleaned data'''
data = pd.DataFrame(clean_data, columns=col_name)



'''change the data from being a string to a float datatype'''
data = data.astype(float)

'''print out specfic coloumns of the dataframe'''
#print(data['Force'])
#print(data['Displacement'])
#print(data['Time'])
#print(data['Count'])


max = data[5000:6000].max()
print(max['Force'])
min = data[5000:6000].min()
print(min['Force'])


'''take subset of data where the force value is greater than zero'''
#data = data.loc[(data['Force'] > min['Force']) & (data['Force'] < max['Force'])]

'''try to take out the data after the specimen has broken'''
data = data[0:-75]

'''Stress calculation'''
data['Stress'] = data['Force'] / area

'''Strain Calculation'''
data['Strain'] = data['Displacement'] / g_len

'''plot Force vs. Displacement'''
data.plot(y='Force', x = 'Displacement')

'''plot Stress vs. Strain'''
data.plot(y='Stress', x='Strain')

#plt.show()

data.to_excel('data/' + file_name+'.xls')