import pandas as pd
import numpy as np
import os
import sys


og = pd.read_excel('raw_data/allagegroups.xlsx', sheet_name='Sheet1')
df = pd.DataFrame(columns=['Time', 'Event', 'Name', 'Age', 'Date', 'Meet'])
print(df)
currentRow = {}
for index, row in og.iterrows():
    if pd.isnull(og.iloc[index]['Dist']) and len(og.iloc[index]['Time']) != 0:
        name = list(filter(None, og.iloc[index]['Time'].split(' ')))
        name.remove('(Yr:')
        print(name)
