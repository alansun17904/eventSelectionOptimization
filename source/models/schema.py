import pandas as pd
import os
from source.filter.scoring import create_comparison_db


class Schema:
    def __init__(self, swimmers: list, allevents, limitdate, filterF, score_func):
        """
        :param swimmers: SwimmerList from settings.py
        :param allevents: The enum class declared in settings.py
        :param limitdate: datetime object that marks the ending date for which all swims will be considered
        :param filterF: The function that will be used to filter all of the swims (filter/filters.py)
        :param score: The score function that will be used to calculate contribution (filter/scoring.py)
        """
        # Schema.changeToDataDirectory()
        # read in excel sheet with all historic data
        originalData = pd.read_excel('data/in/processed.xlsx', sheet_name='Sheet1')
        # convert fields `time` to datetime objects
        originalData['Time'] = originalData['Time'].apply(Schema.timeConversion)
        originalData['Date'] = pd.to_datetime(originalData['Date'])   # convert fields `date` to datetime objects
        originalData = originalData[originalData['Date'] < limitdate]  # find all times swam before the limitdate
        # creates a new df with unique entries for each swimmer
        comparison_df = create_comparison_db(originalData, filterF)
        self.schema = []  # stores the point contribution for each swimmer in each event
        self.timeSchema = []   # stores the times of each swimmer in each event 
        for swimmer in swimmers:
            targetSwimmerScore = []  
            targetSwimmerTime = []
            for race in list(allevents):
                event, time = filterF(originalData, swimmer, race.name)
                score = score_func(originalData, comparison_df, swimmer, race.name)
                targetSwimmerScore.append(score)
                targetSwimmerTime.append(time)
            self.schema.append(targetSwimmerScore)
            self.timeSchema.append(targetSwimmerTime)
        self.schema = pd.DataFrame(self.schema, index=swimmers, columns=[v.name for v in list(allevents)])
        self.timeSchema = pd.DataFrame(self.timeSchema, index=swimmers, columns=[v.name for v in list(allevents)])

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
            os.chdir('..')
            os.chdir('..')
            os.chdir('data')
            os.chdir('in')
        except OSError:
            print('Could not change the current working directory')


