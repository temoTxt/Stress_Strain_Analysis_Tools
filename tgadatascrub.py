import pandas as pd
import re
import matplotlib.pyplot as pyplt
import os

TGA_Output = 'File Name \t Dose (MGy) \t Row Location \t Decomp Temp (C) \n'
'''get file locations of the raw .dat file'''
for i in range(0, 3):
    thickness = ['3.3302_', '1.27_', '0.254_']
    file_front = 'data/TGA_import-' + str(thickness[i])
    # print(file_front)
    for j in range(0, 7):
        dose = ['0mgy', '0.1mgy', '0.2mgy', '0.3mgy', '0.5mgy', '0.6mgy', '1.0mgy']
        file_middle = file_front + str(dose[j]) + '_tga_r('
        # print(file_middle)
        for replicates in range(1, 16):
            file = file_middle + str(replicates) + ').txt'
            split_filename = file.split('_')
            dose = split_filename[2]


            '''get file name to write output file'''
            file_name = os.path.splitext(file)[0]
            file_name = os.path.basename(file_name)
            print(file_name)

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
                        line = line.replace('\t', '  ')
                        # print(line)

                        '''strip out the \n at the end of each line'''
                        line = line.rstrip()

                        '''check to see if there are any letters in the string. If there are not it must be a data line'''
                        if re.search('[a-zA-Z]', line) == None:

                            '''if there is actually values in the line then we add it to our cleaned data list object'''
                            if len(line) > 4:
                                '''split the line into multiple elements using the comma as the anchor point'''
                                line = line.split('  ')

                                '''add this line to the list object for ingest into Pandas'''
                                clean_data.append(line)

                    col_name = ['Number', 'Time', 'Temp_C', 'DTA', 'TG-Weight','DTG']

                    '''create pandas dataframe with the cleaned data'''
                    data = pd.DataFrame(clean_data, columns=col_name)
                    # print(data.head())
                    '''change the data from being a string to a float datatype'''
                    data = data.astype(float)

                    '''convert temperature to kelvin - will need it for activation energy'''
                    temp_kelvin = data['Temp_C']+273
                    '''add a new column for the smoothed data y_avg from the window 35'''
                    data.insert(6, 'Temp_K', temp_kelvin)
                    #print(data.head(5))

                    '''calculate 5% of the weight'''
                    five_percent_weight = data['TG-Weight'][0]-(data['TG-Weight'][0]*0.05)
                    print(five_percent_weight)
                    #data.round(2)['TG-Weight']
                    #decomp_temp = data['Temp_C'].where(data['TG-Weight']==five_percent_weight)
                    decomp_temp = data.iloc[(data['TG-Weight'] - five_percent_weight).abs().argsort()[:1]]['Temp_C']
                    # if decomp_temp
                    print(decomp_temp)

                    '''calculate percent decomposition'''
                    #data['percent_weight_loss']=round(data['TG-Weight']*100/data['TG-Weight'][0],0)

                    pyplt.plot(data['Temp_C'],data['TG-Weight'])
                    #pyplt.xlabel('Temperature (C)')
                    #pyplt.ylabel('Percent Weight Loss (%)')
                    #pyplt.show()
                    #pyplt.savefig('data/processed_data_files/tensile/' + file_name + '.png')
                    #pyplt.clf()
                    #pyplt.close()
                    TGA_Output = TGA_Output + str(file_name) + '\t' + str(dose) + '\t' + str(decomp_temp) + '\n'
                    data.to_excel('data/processed_data_files/tensile/' + file_name + '.xlsx')
            True

print(TGA_Output)



