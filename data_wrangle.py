import pandas as pd
import numpy as np
import os
from pprint import pprint
import sys
from swimmer import SCORE, SWIMMERS, SwimmingRace
from swimmer import Filter


class ScoreSchema:
    def __init__(self):
        originalData = pd.read_excel('data/ilikeswim.xlsx', sheet_name='bois')
        originalData['Time'] = originalData['Time'].apply(ScoreSchema.timeConversion)
        self.schema = []
        self.timeSchema = originalData
        for swimmer in SWIMMERS:
            targetSwimmer = []
            for race in list(SwimmingRace):
                event, score = Filter.takeMax(originalData, swimmer, race.name)
                targetSwimmer.append(score)
            self.schema.append(targetSwimmer)
        self.schema = pd.DataFrame(self.schema, index=SWIMMERS, columns=[v.name for v in list(SwimmingRace)])
    @staticmethod
    def timeConversion(time):
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


