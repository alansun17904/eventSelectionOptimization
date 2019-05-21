import pandas as pd
from datetime import datetime
import numpy as np
import os
import sys


dist = {
    '50': '50m',
    '100': '100m',
    '200': '200m',
    '400': '400m'
}
stroke = {
    'Free': 'FR',
    'IM': 'IM',
    'Breast': 'BR',
    'Back': 'BA',
    'Fly': 'FLY'
}

og = pd.read_excel('raw_data/allagegroups.xlsx', sheet_name='Sheet1')
# creating a new dataframe to fit in all the data
df = pd.DataFrame(columns=['Rank', 'Time', 'Event', 'Name', 'Age', 'Date', 'Meet'])
listdf = []
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
    currentRow["Rank"] = 0  # Can't determine locally
    currentRow["Name"] = currentName
    currentRow["Age"] = 0  # Too annoying to get the age from data especially when raw is not consistent
    if type(og.iloc[index]['Meet']) == float:
        break
    currentRow["Meet"] = og.iloc[index]['Meet'].strip()
    currentRow["Time"] = og.iloc[index]['Time'].strip()
    currentRow["Event"] = stroke[og.iloc[index]['Event']] + dist[str(int(og.iloc[index]['Dist']))]
    if type(og.iloc[index]['Date']) == str:
        currentRow["Date"] = datetime.strptime(og.iloc[index]['Date'], '%m/%d/%Y')
    else:
        currentRow["Date"] = og.iloc[index]['Date']

    listdf.append(currentRow)
    currentRow = {}
print(listdf)

df = pd.DataFrame(listdf)
df.to_excel("data/processed.xlsx")
