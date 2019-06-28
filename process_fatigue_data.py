import pandas as pd
import numpy as np
import scipy.integrate as integrate

data = pd.read_excel('/home/tmorris/ResearchReader/articles/Fatigue Data/95% UTS/0.3302 Solid/95% UTS 0.3302 Solid.xlsx'
                     , header=1)

pos = []
neg = []
'''group by what cycle you are on'''
for cycle, df_cycle in data.groupby('Cycle'):
    #print(df_cycle.head())

    '''grab the data for the y vs. x relations of Force vs. Displacement'''
    y = df_cycle['Normalized Force (kN)'].to_list()
    #print(y)

    x = df_cycle['Normalized Displacement (mm)'].to_list()
    #print(x)

    '''fit a 3rd order polynomial to the cycle data'''
    z = np.polyfit(x, y, 3)
    #print(z)

    '''integrate the order polynomial from the first x value (x[0]) to the last value (x[-1])'''
    [sum, error] = result = integrate.quad(lambda x: z[0] * x**3 + z[1] * x**2 + z[2] + x +z[1] + z[0], x[0], x[-1])

    #print(sum)

    if sum > 0:
        pos.append(sum)
    elif sum < 0:
        neg.append(sum)
    else:
        print('You done fucked up')


total = np.sum(pos) + np.sum(neg)

print(total)