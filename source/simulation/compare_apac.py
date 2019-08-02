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
        # original_data['Name'] = original_data['Name'].apply(lambda s: f'{s.split(",")[1].strip()} '
        #                                                               f'{s.split(",")[0].strip()}')
        original_data = original_data[original_data['Date'] == self.year]
        # limits initialization gender to the one in settings.py
        original_data = original_data[original_data['Gender'] == GENDER]
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
            for col in range(len(times)):  # only add times that are apart of the optimal solution
                r_time_schema.append(list(times.iloc[row])[col] * self.optimal_solution[row][col])
            self.time_schema.append(r_time_schema)

    def check_apac(self, swimmer, swimming_race):
        """
        Checks if a swimmer has swam a certain race at that year's APAC championship.
        :param swimmer: (str) the name of the swimmer.
        :param swimming_race: (str) the name of the event that is being checked.
        :return: (time, score) the time that they got if they made finals and along with the score
        if they did not make finals then the attached time is the time they swam in prelims.
        If the swimmer did not swim this event then the time value will be -1 and the score value
        will also be -1.
        """
        swimmer_name = f'{swimmer.split()[1]}, {swimmer.split()[0]}'
        prelim_races = self.apac_with_team[(self.apac_with_team['Name'] == swimmer_name) &
                                    (self.apac_with_team['Event'] == swimming_race) &
                                    (self.apac_with_team['Prelim/Finals'] == 'Prelim')]
        finals_races = self.apac_with_team[(self.apac_with_team['Name'] == swimmer_name) &
                                    (self.apac_with_team['Event'] == swimming_race) &
                                    (self.apac_with_team['Prelim/Finals'] == 'Finals')]
        if len(finals_races) > 1:
            raise RuntimeError(f'More than one race found for swimmer {swimmer_name} at event {swimming_race}')
        elif len(prelim_races) == 0:  # they didnt swim a prelim race
            return (-1, -1),
        elif prelim_races and finals_races:  # if they made prelims and finals
            return ((prelim_races.iloc[0]['Time'], prelim_races.iloc[0]['Rank']),
                    (-1, -1))
        else:
            return ((prelim_races.iloc[0]['Time'], prelim_races.iloc[0]['Rank']),
                    (finals_races.iloc[0]['Time'], finals_races.iloc[0]['Rank']))

    def add_race(self, swimmer_name, event_name, previous_race_status, time=0):
        """
        Adds a swimmers entry into the APAC database
        :param previous_race_status: (tuple) with the status of each swimmers history and the races that they
        have swam at apac.
        :param prelims: (bool) True if the person swam the prelims for this race.
        :param finals: (bool) True if the person swam the prelims and the finals for this race.
        :param time: (float) only provide a time if both prelims & fianls are false.
        :return: None
        """
        if previous_race_status[0][0] == -1:  # never swam this event before
            self.apac = self.apac.append({
                'SchoolSerial': 'ISB',
                'Gender': GENDER,
                'Name': swimmer_name,
                'Event': event_name,
                'Time': time,
                'Rank': 0,
                'Age': 0,
                'Date': self.year,
                'Prelim/Finals': 'Prelim'
            }, ignore_index=True)
        elif previous_race_status[1][0] == -1:  # they only swam prelims but didn't make finals
            self.apac = self.apac.append({
                'SchoolSerial': 'ISB',
                'Gender': GENDER,
                'Name': swimmer_name,
                'Event': event_name,
                'Time': previous_race_status[0][0],
                'Rank': previous_race_status[0][1],
                'Age': 0,
                'Date': self.year,
                'Prelim/Finals': 'Prelim'  # since this swimmer has already swam this event before
                # we are going to take the exact amount of points that they scored at the meet
            }, ignore_index=True)
        else:  # they swam prelims and then ended up making finals
            self.apac = self.apac.append({
                'SchoolSerial': 'ISB',
                'Gender': GENDER,
                'Name': swimmer_name,
                'Event': event_name,
                'Time': previous_race_status[1][0],
                'Rank': previous_race_status[1][1],
                'Age': 0,
                'Date': self.year,
                'Prelim/Finals': 'Finals'
            })
            previous_race_status = (previous_race_status[0], (-1, -1))
            self.add_race(swimmer_name, event_name, previous_race_status)


    def run_simulation(self):
        self.read_apac_data()
        self._create_new_time_schema()
        for row in range(len(self.time_schema)):
            for col in range(len(self.time_schema[row])):
                if self.time_schema[row][col] == 0:  #
                    continue
                previous_race = self.check_apac(self._SWIMMERS[row], SwimmingRace(col + 1).name)
                if previous_race[0][0] == -1:  # never swam this event before
                    self.add_race(self._SWIMMERS[row], SwimmingRace(col + 1).name,
                                  previous_race, time=self.time_schema[row][col])
                else:
                    self.add_race(self._SWIMMERS[row], SwimmingRace(col + 1).name,
                                  previous_race)
        return self.apac

    def score_apac(self):
        """
        uses the apac dataframe to calculate the subscores for each team.
        :return: Writes the end result of each optimization to the file in the data/out/opt directory
        also prints the team scores to the console.
        """
        team_scores = {}
        # give each person a time based on their prelim performance
        for row in range(len(self.apac)):  # give each person a score based on their time
            rank = len(self.apac[(self.apac['Gender'] == GENDER) & (self.apac['Event'] == self.apac['Event'][row])
                             & (self.apac['Time'] < self.apac['Time'][row])
                             & (self.apac['Prelim/Finals'] == 'Prelim')]) + 1
            self.apac.at[row, 'Rank'] = score(rank)

        # loop through all the teams and add them to the team_scores dictionary
        for team in self.apac['SchoolSerial'].unique():
            sum_df = self.apac[(self.apac['SchoolSerial'] == team) & (self.apac['Gender'] == GENDER)]
            if team not in team_scores:
                team_scores[team] = sum_df['Rank'].sum()

        return team_scores
