## This file is no longer used. It was used to store the csv files using a different separator initially

import pandas as pd
import os

INPUT_DIR = '../raw_scrape/'
editorials = pd.read_csv('master.csv')
# content should not be empty (if you do not want assert, remove the rows which don't have any content)
assert editorials.isnull().values.sum() == 0

single = editorials[~editorials.Content.str.contains('\n')]

f = open('single.txt','w')
for index,row in single.iterrows():
    s = ''
    s += row['Link'] + ' '
    s += row['Year'] + '/'
    s += row['Month'] + '/'
    s += row['Date'] + '\n'
    f.write(s)
f.close()
