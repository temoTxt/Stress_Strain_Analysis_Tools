import os

sncurve_data = 'data/output'
sncurve_file = os.path.splitext(sncurve_data)[0] + '.txt'
sncurve_path = open('data/output', 'w')
print(sncurve_file)

'''seperate blob into lines of text'''
lines = sncurve_path.readlines()

'''create list object to put in only numerical data'''
clean_data = []

'''go line by line to scrub header data'''
for line in lines:

    '''convert all \t to an actual tab in the data'''
    line = line.replace(' ', ',')
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