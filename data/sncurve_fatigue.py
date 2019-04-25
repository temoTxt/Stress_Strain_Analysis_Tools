import os
import csv
import sys
import pandas as pd

'''don't need data/ at the beginning b/c the py script is inside the data folder'''
'''if you need to move the py script into the parent directory remember to add the path back in'''
'''the txt file is tab delimitated'''
sncurve_data_txt = 'tesile_output.txt'
sncurve_data_csv = 'tensile_outputdata.csv'
with open(sncurve_data_txt, 'r') as infile, open(sncurve_data_csv, 'w') as outfile:
    stripped = (line.strip() for line in infile)
    lines = (line.split("\t") for line in stripped if line)
    writer = csv.writer(outfile)
    writer.writerows(lines)
print(outfile)

col_name = Tensile = ['File Name', 'Printer', 'UTS (MPa)', 'Stress at Failure (MPa)', 'Strain at Failure (mm/mm)']

'''create pandas dataframe with the cleaned data'''
data = pd.read_csv(outfile)
print(data.head())

