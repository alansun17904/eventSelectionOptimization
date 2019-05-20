import pandas as pd
import numpy as np
import os
from wrangle import ScoreSchema
from swimmer import SCORE, SWIMMERS, SwimmingRace, Filter
from optimize import OUTPUTDF


class Simulation:
    def __init__(self, timeSchema, strategySchema, year: str, school, removeSelf=True, \
                 prelims=True, gender='BOYS'):
        # schema of the times of all the people being schemaed
        self.timeSchema = timeSchema
        # the selection of events
        self.strategySchema = strategySchema
        # if prelims / finals are going to be considered or only finals
        self.prelims = prelims
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
        if type(time) == str and len(time.split('.')) == 2:
            return float(time)
        if type(time) == float or type(time) == int:
            return float(time)
        s = time.split('.')
        return float(s[0])*60 + float('.'.join(s[1:]))
    
    def searchTime(self, name, event):
        """
        name: str
        event: str, based on the name of the enums defined in SwimmingRace
        It finds the time of the corresponding swimmer in a certain
        event and returns the time as a float.
        """
        time = self.timeSchema[(self.timeSchema['Name'] == name) \
            & (self.timeSchema['Event'] == event)]
        if len(time) == 0:
            return self.searchTime(name, Filter.skillFinder[event])
        return time.iloc[0]['Time']
    
    def calculateRelayTime(self, relayEvent='IM', adjustment=0.):
        """
        adjustment (float): adds a amount of time to the final calculated relay
        time based on the how well the optimizer thinks that the team is 
        going to perform.
        relayEvent (str): the name of the relay event being calculated. 
        By default it is set to calculate the time of the IM relay. Other
        than the IM relay this parameter needs the name from the enums of 
        SwimmingRace.
        :return (float): the final time in seconds.
        """
        compositeTime = 0
        if relayEvent == 'IM':
            for leg in ['IMRelay4P50_FR', 'IMRelay4P50_BR', \
                        'IMRelay4P50_BA', 'IMRelay4P50_FLY']:
                for swimmer in SWIMMERS:
                    if self.strategySchema[leg][swimmer] == 1:
                        compositeTime += self.searchTime(swimmer, leg) + adjustment
        else:
            for swimmer in SWIMMERS:
                if self.strategySchema[relayEvent][swimmer] == 1:
                    compositeTime += self.searchTime(swimmer, relayEvent) + adjustment
        return compositeTime
    
    def compareTime(self, name, event):
        """
        Compares the time of swimmer with the league / competition.
        :return (int): the rank of the swimmer were to swim with
        the rest of the competition.
        """
        time = self.searchTime(name, event)
        if self.prelimes == True:
            eventPrelims = self.test[(self.test['Event']==event) & \
                (self.test['Prelim/Final']=='Prelim')]
            # rank = eventPrelims[eventPrelims['Time']<]
        return

    def simulate(self):
        """
        runs the simulation
        :returns (int): the score for the simulation.
        """
        return

if __name__ == '__main__':
    # schema = ScoreSchema()
    # s = Simulation(schema.timeSchema, OUTPUTDF, '2018', 'ISB', prelims=False)
    # print(s.searchTime('Miles Huang', 'FR50m'))
    # print(s.calculateRelayTime()) 
    print(Simulation.timeConversionAPAC('29.00'))