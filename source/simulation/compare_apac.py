from source.lp.optimize import Optimize
from source.models.schema import Schema
from source.settings import SWIMMERS, SwimmingRace, score, GENDER
import pandas as pd


class Simulation:
    def __init__(self, year, optimize: Optimize, remove_self=True):
        """
        :param year: (int) APAC year that is being compared to.
        :param optimize: optimize object that contains the optimal solution
        """
        if 'optimal' not in dir(optimize):
            optimize.optimize()
        self.optimize = optimize
        self.remove_self = remove_self
        self._SWIMMERS = SWIMMERS
        self.optimal_solution = optimize.optimal
        self.year = year
        self.apac = []
        self.time_schema = []

    @staticmethod
    def apac_time_conversion(time):
        if type(time) == float or type(time) == int:
            return time
        else:
            t_components = time.split('.')
            if len(t_components) == 3:
                return int(t_components[0]) * 60 + int(t_components[1]) + int(t_components[2]) / 100
            elif len(t_components) == 2:
                return int(t_components[0]) + int(t_components[1]) / 100

    def read_apac_data(self):
        original_data = pd.read_excel('data/in/APAC_all.xlsx', sheet_name='Sheet1')
        original_data['Time'] = original_data['Time'].apply(Simulation.apac_time_conversion)
        original_data['Date'] = original_data['Date'].apply(lambda s: int(str(s)[0:4]))
        original_data = original_data[original_data['Date'] == self.year]
        self.apac_with_team = original_data  # apac data with the team that is being optimized
        # apac data without optimize team
        self.apac = original_data[original_data['SchoolSerial'] != 'ISB'] if self.remove_self else original_data

    def _create_new_time_schema(self):
        """
        Generates a time schema in the form of a two-dimensional array where the entries are either
        0 or a float with the swimmers time. Multiplies the components of the time matrix and the
        final optimization matrix.
        :return: None, adds the newly created time_schema to the `time_schema` attribute.
        """
        times = self.optimize.score.timeSchema
        # TODO: able to write this in a nested list comprehension

        for row in range(len(times)):
            r_time_schema = []
            for col in range(len(times)):
                r_time_schema.append(list(times.iloc[row])[col] * self.optimal_solution[row][col])
            self.time_schema.append(r_time_schema)

    def check_apac(self, swimmer, swimming_race):
        """
        Checks if a swimmer has swam a certain race at that year's APAC championship.
        :param swimmer: (str) the name of the swimmer.
        :param swimming_race: (str) the event that is being checked.
        :return: (time, score) the time that they got if they made finals and along with the score
        if they did not make finals then the attached time is the time they swam in prelims.
        If the swimmer did not swim this event then the time value will be -1 and the score value
        will also be -1.
        """
        races = self.apac_with_team[(self.apac_with_team['Name'] == swimmer) &
                                    (self.apac_with_team['Event'] == swimming_race) &
                                    (self.apac_with_team['Prelim/Finals'] == 'Finals')]
        if len(races) > 1:
            raise RuntimeError(f'More than one race found for swimmer {swimmer} at event {swimming_race}')
        elif len(races) == 0:
            return -1, -1
        else:
            return races.iloc[0]['Time'], score(races.iloc[0]['Rank'])

    def score_apac(self, swimmer, swimming_race, time):
        previously_swam = self.check_apac(swimmer, swimming_race)
        if previously_swam[0] == -1:
            # First compare with prelims time
            # FIXME: make the gender variable
            prelim_races = self.apac[(self.apac['Event'] == swimming_race) & (self.apac['Gender'] == GENDER) &
                                     (self.apac['Time'] < time)]
            if len(prelim_races) + 1 > 12:  # if the swimmer did not make finals
                return time, 0
            else:  # if the swimmer made finals compare with finals time
                finals_races = self.apac[(self.apac[''])]
        else:
            return previously_swam

    def run_simulation(self):
        self.read_apac_data()
        self._create_new_time_schema()
        for row in range(len(self.time_schema)):
            for col in range(len(self.time_schema[row])):
                if self.time_schema[row][col] == 0:
                    continue
                previous_race = self.check_apac(self._SWIMMERS[row], SwimmingRace(col + 1).name)
                if previous_race[0] == -1:  # never swam this event before
                    self.apac.append({
                        'SchoolSerial': 'ISB',
                        'Gender': GENDER,
                        'Name': self._SWIMMERS[row],
                        'Event': SwimmingRace(col + 1).name,
                        'Time': self.time_schema[row][col],
                        'Rank': 0,
                        'Age': 0,
                        'Date': self.year,
                        'Prelim/Finals': 'Finals'
                    }, ignore_index=True)
        return self.apac


if __name__ == '__main__':
    print(Simulation.apac_time_conversion('34.29'))
