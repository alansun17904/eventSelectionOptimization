import pandas as pd
import numpy as np
import os
from data_wrangle import ScoreSchema
from swimmer import SCORE, SWIMMERS, SwimmingRace




class Simulation:
    def __init__(self, timeSchema, strategySchema, year: str, school, removeSelf=True, \
                 prelims=True, gender='BOYS'):
        print(os.getcwd())
        self.timeSchema = timeSchema
        self.strategySchema = strategySchema
        originalData = pd.read_excel('data/APAC_all.xlsx', sheet_name="Sheet1")
        originalData['Time'] = originalData['Time'].apply(Simulation.timeConversionAPAC)
        originalData['Date'] = originalData['Date'].apply(lambda s: str(s)[:4])
        self.test = originalData[originalData['Date']==year]
        if removeSelf == True:
            self.test = self.test[self.test['SchoolSerial']!=school]
        if prelims == False:
            self.test = self.test[self.test['Prelim/Finals']!='Prelim']
        self.test = self.test[self.test['Gender']==gender]

    @staticmethod
    def timeConversionAPAC(time):
        if type(time) == float or type(time) == int:
            return float(time)
        s = time.split('.')
        return float(s[0])*60 + float('.'.join(s[1:]))
    
    def searchTime(self, name, event):
        """
        name: str
        event: str, based on the name of the enums defined in SwimmingRace
        It finds the time of the corresponding swimmer in a certain
        event and returns the time and event in a tuple.
        (event: str, time: int)
        """
        time = self.timeSchema[(self.timeSchema['Name'] == name) \
            & (self.timeSchema['Event'] == event)].iloc[0]['Time']
        return (event, time)
    
    def calculateRelayTime(self, adjustment=0.):
        """
        adjustment (float): adds a amount of time to the final calculated relay
        time based on the how well the optimizer thinks that the team is 
        going to perform.
        :return (float): the final time in seconds.
        """
        return
    
    def compareTime(self, name, event, prelims=True):
        """
        Compares the time of swimmer with the league / competition.
        :return (int): the rank of the swimmer were to swim with
        the rest of the competition.
        """
        return

    def simulate(self):
        return

if __name__ == '__main__':
    schema = ScoreSchema()
    s = Simulation(schema.timeSchema, 2, '2018', 'ISB', prelims=False)
    print(s.searchTime('Miles Huang', 'FR50m'))
    