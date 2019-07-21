import pulp
import datetime
from source.models.schema import Schema


class Optimize:
    def __init__(self, swimmers: list, events: list, min_relays: int, max_relays: int, score: Schema,
                 ind_events: int, ind_relay_events: int, individualEvents: list, IMrelay: list, team_num: int,
                 custom_lock = [[]], custom_unlock = [[]]):
        """
        Constructuor that creates a new LP Problem using the `pulp` package.
        :param swimmers: A list of all the names (str) of the swimmers being optimzed.
        :param events: A list of all the events (str) of all the events being optmized.
        :param min_relays: The minimum number of relays that the team is going to enter.
        :param max_relays: The maximum number of relays that the team is allowed to enter.
        :param score: A ScoreSchema Object that is made to calculate an individuals contribution.
        :param ind_events: The maximum number of individual events that an individual is allowed to participate in.
        :param ind_relay_events: The total maximum number of events (relay + individual) that and individual is
        allowed to participate in.
        :param individualEvents: A list of all of the individual events being optimized.
        :param IMrelay: A list of the order of the IM Relay... It is assumed that the IM relay is the
        4 x 50 medeley relay.
        :param team_num: The maximum number of people a team is allowed to send in an event.
        :param custom_lock: A nested list that contains the swimmer and the event he or she must be place in.
        :param custom_unlock: A nested list that contains the swimmer and the event he or she must not be placed in.
        """
        self.problem = pulp.LpProblem('Swimming score maximizing problem', pulp.LpMaximize)
        self._SWIMMERS = swimmers
        self.score = score
        self._EVENTS = events
        self.optimal = []
        # Variable Creation
        self.swimmerStatus = pulp.LpVariable.dicts('swimmerStatus',
                                                   ((swimmer, event) for swimmer in self._SWIMMERS
                                                    for event in self._EVENTS), cat='Binary')
        self.numberOfRelays = pulp.LpVariable('numberOfRelays', lowBound=min_relays,
                                              upBound=max_relays, cat=pulp.LpInteger)
        # COST FUNCTION
        # TODO: need to fix this the schema class up
        self.problem += pulp.lpSum([self.swimmerStatus[(s, e)] * score.schema.loc[s, e]
                                    for e in self._EVENTS for s in self._SWIMMERS])

        # CONSTRAINTS
        for swimmer in self._SWIMMERS:
            # individual constraint1: where the sum of a swimmer's individual events must not exceed ind_events
            self.problem += pulp.lpSum([self.swimmerStatus[(swimmer, e)] for e in individualEvents]) <= ind_events
            # individual constraint2: where the sum of a swimmer's individual+relay events must not
            # exceed ind_events + ind_relay_events
            self.problem += pulp.lpSum([self.swimmerStatus[(swimmer, e)] for e in self._EVENTS]) <= ind_relay_events
            # relay constraint3: you cannot be in the IMRelay4P50 more than 1 time.
            self.problem += pulp.lpSum([self.swimmerStatus[(swimmer, e)] for e in IMrelay]) <= 1

        for e in individualEvents:
            # team constraint1: where the amount of swimmers per individual event per team must not exceed team_num
            self.problem += pulp.lpSum([self.swimmerStatus[(swimmer, e)] for swimmer in self._SWIMMERS]) <= team_num

        # RELAY CONSTRAINTS
        self.problem += pulp.lpSum([self.swimmerStatus[(swimmer, 'FRRelay4P50')] for swimmer in self._SWIMMERS]) == 4 * self.numberOfRelays
        self.problem += pulp.lpSum([self.swimmerStatus[(swimmer, 'FRRelay4P100')] for swimmer in self._SWIMMERS]) == 4 * self.numberOfRelays
        # relay constraint2: there must be 4 people for IMRelay4P50
        self.problem += pulp.lpSum([self.swimmerStatus[(s, e)] for e in IMrelay for s in self._SWIMMERS]) == 4 * self.numberOfRelays
        # relay constraint4: IMRelay4P50 must be 4 people swimming different strokes
        for stroke in IMrelay:
            self.problem += pulp.lpSum([self.swimmerStatus[(s, stroke)]
                                        for s in self._SWIMMERS]) <= self.numberOfRelays

    def optimize(self):
        # LP Solve
        self.problem.solve()
        print(pulp.LpStatus[self.problem.status])
        # Display Results
        output = []
        for swimmer in self._SWIMMERS:
            row = []
            for s, e in self.swimmerStatus:
                if swimmer == s:
                    row.append(self.swimmerStatus[(s, e)].varValue)
                else:
                    continue
            output.append(row)
        self.optimal = output
        return output

    def write_optimal(self):
        f_out = open(f'data/out/{datetime.datetime.now().strftime("%m-%d-%y<>%H:%M:%S")}.txt', 'w+')
        header = ' ' * 15 + ''.join([e.rjust(15, ' ') for e in self._EVENTS]) + '\n'
        f_out.write(header)
        for row in range(len(self.optimal)):
            output_row = list(map(lambda s: str(s).rjust(15, ' '), self.optimal[row]))
            f_out.write(self._SWIMMERS[row].rjust(15, ' ') + ''.join(output_row) + '\n')
        f_out.write('\n')
        for row in range(len(self.score.timeSchema)):
            output_row = list(map(lambda s: str(round(s, 2)).rjust(15, ' '), list(self.score.timeSchema.iloc[row])))
            f_out.write(self._SWIMMERS[row].rjust(15, ' ') + ''.join(output_row) + '\n')

        f_out.close()
