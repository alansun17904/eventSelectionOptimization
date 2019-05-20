import pandas as pd
import numpy as np
import os
import sys


og = pd.read_excel('raw_data/allagegroups.xlsx', sheet_name='Sheet1')
# creating a new dataframe to fit in all the data
df = pd.DataFrame(columns=['Time', 'Event', 'Name', 'Age', 'Date', 'Meet'])
print(df)
currentRow = {}
currentName = ""
for index, row in og.iterrows():
    if pd.isnull(og.iloc[index]['Dist']) and not pd.isnull(og.iloc[index]['Time']):
        # get name
        name = list(filter(None, og.iloc[index]['Time'].split(' ')))
        if name[0] == "*I":
            currentName = name[1] + " " + name[2]
        else:
            currentName = name[0] + " " + name[1]
        continue
    currentRow["Name"] = name
    currentRow["Time"] = og.iloc[index]['Time']
    currentRow["Date"] = og.iloc[index]['Date']