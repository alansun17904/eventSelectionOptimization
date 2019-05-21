import pulp
from swimmer import SWIMMERS
from swimmer import SwimmingRace
from wrangle import ScoreSchema
import pandas as pd


class Model:
    def __init__(self, swimmers: list, events: list, min_relays: int, max_relays: int, score,
                 ind_events: int, ind_relay_events: int, individualEvents: list, IMrelay: list, team_num: int):
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
        4x50 medeley relay.
        :param team_num: The maximum number of people a team is allowed to send in an event.
        """
        self.problem = pulp.LpProblem('Swimming score maximizing problem', pulp.LpMaximize)
        self._SWIMMERS = swimmers
        self._EVENTS = events
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
            self.problem += pulp.lpSum([self.swimmerStatus[(s, stroke)] for s in self._SWIMMERS]) <= self.numberOfRelays

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
                else: continue
            output.append(row)
        return output


if __name__ == "__main__":
    allEvents = [v.name for v in list(SwimmingRace)]
    individualEvents = [v.name for v in list(SwimmingRace) if v.value < 13]
    relayEvents = [v.name for v in list(SwimmingRace) if v.value >= 13]
    IMrelay = [v.name for v in list(SwimmingRace) if v.value >= 15]
    scoreSchema = ScoreSchema()
    # create new lp problem
    model = Model(SWIMMERS, allEvents, min_relays=1, max_relays=2, score=scoreSchema, ind_events=4,
                  ind_relay_events=5, individualEvents=individualEvents, IMrelay=IMrelay, team_num=4)
    strategy = pd.DataFrame(model.optimize(), index=SWIMMERS, columns=allEvents)
    # TODO: Add a time schema to see the times chosen for the program


    # Write to excel
    strategy.to_excel('data/schema.xlsx', sheet_name="Strategy")
    scoreSchema.schema.to_excel('data/scoring.xlsx', sheet_name="Scoring")

