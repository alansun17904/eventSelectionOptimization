from source.lp.optimize import Optimize
from source.settings import SWIMMERS, SwimmingRace, score, GENDER
import pandas as pd


class Simulation:
    def __init__(self, year, optimize: Optimize, remove_self=True):
        """
        :param year: (int) league year that is being compared to.
        :param optimize: optimize object that contains the optimal solution
        """
        if 'optimal' not in dir(optimize):
            optimize.optimize()
        self.optimize = optimize
        self.remove_self = remove_self
        self._SWIMMERS = SWIMMERS
        self.optimal_solution = optimize.optimal
        self.year = year
        self.league = []
        self.time_schema = []

    @staticmethod
    def league_time_conversion(time):
        if type(time) == float or type(time) == int:
            return time
        else:
            t_components = time.split('.')
            if len(t_components) == 3:
                return int(t_components[0]) * 60 + int(t_components[1]) + int(t_components[2]) / 100
            elif len(t_components) == 2:
                return int(t_components[0]) + int(t_components[1]) / 100

    def read_league_data(self):
        relays = [SwimmingRace(13).name, SwimmingRace(14).name, SwimmingRace(15).name,
                  SwimmingRace(16).name, SwimmingRace(17).name, SwimmingRace(18).name]
        original_data = pd.read_excel('data/in/league_all.xlsx', sheet_name='Sheet1')
        original_data['Time'] = original_data['Time'].apply(Simulation.league_time_conversion)
        original_data['Date'] = original_data['Date'].apply(lambda s: int(str(s)[0:4]))
        original_data['PendingState'] = '-'
        original_data = original_data[original_data['Date'] == self.year]
        # limits initialization gender to the one in settings.py
        original_data = original_data[original_data['Gender'] == GENDER]
        original_data = original_data[~original_data['Event'].isin(relays)]
        self.league_with_team = original_data  # league data with the team that is being optimized
        # league data without optimize team
        self.league = original_data[original_data['SchoolSerial'] != 'team'] if self.remove_self else original_data

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

    def check_league(self, swimmer, swimming_race):
        """
        Checks if a swimmer has swam a certain race at that year's league championship.
        :param swimmer: (str) the name of the swimmer.
        :param swimming_race: (str) the name of the event that is being checked.
        :return: (time, score) the time that they got if they made finals and along with the score
        if they did not make finals then the attached time is the time they swam in prelims.
        If the swimmer did not swim this event then the time value will be -1 and the score value
        will also be -1.
        """
        swimmer_name = f'{swimmer.split()[1]}, {swimmer.split()[0]}'
        prelim_races = self.league_with_team[(self.league_with_team['Name'] == swimmer_name) &
                                    (self.league_with_team['Event'] == swimming_race) &
                                    (self.league_with_team['Prelim/Finals'] == 'Prelim')]
        finals_races = self.league_with_team[(self.league_with_team['Name'] == swimmer_name) &
                                    (self.league_with_team['Event'] == swimming_race) &
                                    (self.league_with_team['Prelim/Finals'] == 'Finals')]
        if len(finals_races) > 1:
            raise RuntimeError(f'More than one race found for swimmer {swimmer_name} at event {swimming_race}')
        elif len(prelim_races) == 0:  # they didnt swim a prelim race
            return (-1, -1),
        elif len(prelim_races) != 0 and len(finals_races) == 0:  # if they made prelims but not finals
            return ((prelim_races.iloc[0]['Time'], prelim_races.iloc[0]['Rank']),
                    (-1, -1))
        else:
            return ((prelim_races.iloc[0]['Time'], prelim_races.iloc[0]['Rank']),  # prelims time and rank
                    (finals_races.iloc[0]['Time'], finals_races.iloc[0]['Rank']))  # finals time and rank

    def add_race(self, swimmer_name, event_name, previous_race_status, time=0):
        """
        Adds a swimmers entry into the league database
        :param previous_race_status: (tuple) with the status of each swimmers history and the races that they
        have swam at league.
        :param prelims: (bool) True if the person swam the prelims for this race.
        :param finals: (bool) True if the person swam the prelims and the finals for this race.
        :param time: (float) only provide a time if both prelims & finals are false.
        :return: None
        """
        if previous_race_status[0][0] == -1:  # never swam this event before
            self.league = self.league.append({
                'SchoolSerial': 'team',
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
            self.league = self.league.append({
                'SchoolSerial': 'team',
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
            if previous_race_status[1][1] <= 8:
                finals_status = 'Finals_A'
            elif 8 < previous_race_status[1][1] <= 16:
                finals_status = 'Finals_B'
            else:
                finals_status = 'Prelim'
            self.league = self.league.append({
                'SchoolSerial': 'team',
                'Gender': GENDER,
                'Name': swimmer_name,
                'Event': event_name,
                'Time': previous_race_status[1][0],
                'Rank': previous_race_status[1][1],
                'Age': 0,
                'Date': self.year,
                'Prelim/Finals': finals_status
            }, ignore_index=True)

    def run_simulation(self):
        self.read_league_data()
        self._create_new_time_schema()
        for row in range(len(self.time_schema)):
            for col in range(len(self.time_schema[row])):
                if self.time_schema[row][col] == 0:  #
                    continue
                previous_race = self.check_league(self._SWIMMERS[row], SwimmingRace(col + 1).name)
                if previous_race[0][0] == -1:  # never swam this event before
                    self.add_race(self._SWIMMERS[row], SwimmingRace(col + 1).name,
                                  previous_race, time=self.time_schema[row][col])
                else:
                    self.add_race(self._SWIMMERS[row], SwimmingRace(col + 1).name,
                                  previous_race)
        return self.league

    def score_league(self):
        """
        uses the league dataframe to calculate the subscores for each team.
        :return: Writes the end result of each optimization to the file in the data/out/opt directory
        also prints the team scores to the console.
        """
        team_scores = {}
        # give each person a time based on their prelim performance
        for row in range(len(self.league)):  # give each person a score based on their time
            if self.league['Prelim/Finals'][row] == 'Prelim':
                rank = len(self.league[(self.league['Gender'] == GENDER) & (self.league['Event'] == self.league['Event'][row])
                                 & (self.league['Time'] < self.league['Time'][row])
                                 & (self.league['Prelim/Finals'] == 'Prelim')]) + 1
                self.league.at[row, 'Rank'] = 0
                if 8 < rank <= 16:  # split the people that made finals into finals A and finals B
                    finals_status = 'Finals_B'
                elif rank <= 8:
                    finals_status = 'Finals_A'
                else:
                    continue
            else:
                continue
            # change competitor final status to either finals A or finals B
            rindex = self.league.index[(self.league['Event'] == self.league['Event'][row])
                                & (self.league['Name'] == self.league['Name'][row])
                                & (self.league['SchoolSerial'] == self.league['SchoolSerial'][row])
                                & (self.league['Prelim/Finals'] == 'Finals')].tolist()
            if len(rindex) == 0:
                # if the competitor was not originally in the league final for this event
                self.league.at[row, 'PendingState'] = finals_status
            else:
                self.league.at[rindex[0], 'PendingState'] = finals_status

        for row in range(len(self.league)):  # e valuate the results from the finals
            if str(self.league.at[row, 'PendingState']) == 'nan':
                self.league.at[row, 'Rank'] = score(rank)
                continue
            self.league.at[row, 'Prelim/Finals'] = self.league['PendingState'][row]

        for row in range(len(self.league)):
            rank = len(self.league[(self.league['Gender'] == GENDER) & (self.league['Event'] == self.league['Event'][row])
                                 & (self.league['Time'] < self.league['Time'][row])
                                 & (self.league['Prelim/Finals'] == self.league['Prelim/Finals'][row])]) + 1
            if self.league['Prelim/Finals'][row] == 'Finals_B':
                rank += 8

            self.league.at[row, 'Rank'] = score(rank)

        # loop through all the teams and add them to the team_scores dictionary
        for team in self.league['SchoolSerial'].unique():
            sum_df = self.league[(self.league['SchoolSerial'] == team) & (self.league['Gender'] == GENDER)
                               & (self.league['Prelim/Finals'].isin(['Finals_A', 'Finals_B']))]
            if team not in team_scores:
                team_scores[team] = sum_df['Rank'].sum()
        return team_scores
