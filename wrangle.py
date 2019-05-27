import pandas as pd
import numpy as np
import os
from datetime import datetime
from pprint import pprint
import sys
from swimmer import SCORE, SWIMMERS, SwimmingRace
from swimmer import Filter


class ScoreSchema:
    def __init__(self, limitdate):
        originalData = pd.read_excel('data/processed.xlsx', sheet_name='Sheet1')
        originalData['Time'] = originalData['Time'].apply(ScoreSchema.timeConversion)
        print(originalData.iloc[0]['Date'])
        print(limitdate)
        originalData['Date'] = pd.to_datetime(originalData['Date'])
        originalData = originalData[originalData['Date'] < limitdate]
        self.schema = []
        self.timeSchema = []
        for swimmer in SWIMMERS:
            targetSwimmerScore = []
            targetSwimmerTime = []
            for race in list(SwimmingRace):
                event, score, time = Filter.takeMax(originalData, swimmer, race.name)
                targetSwimmerScore.append(score)
                targetSwimmerTime.append(time)
            self.schema.append(targetSwimmerScore)
            self.timeSchema.append(targetSwimmerTime)
        self.schema = pd.DataFrame(self.schema, index=SWIMMERS, columns=[v.name for v in list(SwimmingRace)])
        self.timeSchema = pd.DataFrame(self.timeSchema, index=SWIMMERS, columns=[v.name for v in list(SwimmingRace)])

    @staticmethod
    def timeConversion(time):
        if time[0] == 'x':
            time = time[1:]
        totalTime = 0
        if type(time) == float:
            return time
        for time in time.split(':'):
            if '.' in time:
                totalTime += float(time)
            else:
                totalTime += float(time) * 60
        return totalTime

    @staticmethod
    def changeToDataDirectory():
        try:
            os.chdir('/data/')
        except OSError:
            print('Could not change the current working directory')


