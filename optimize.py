import pandas as pd 
import pulp
import numpy as np
from swimmer import SWIMMERS
from swimmer import SwimmingRace
from wrangle import ScoreSchema


allEvents = [v.name for v in list(SwimmingRace)]
individualEvents = [v.name for v in list(SwimmingRace) if v.value < 13]
relayEvents = [v.name for v in list(SwimmingRace) if v.value >= 13]
IMrelay = [v.name for v in list(SwimmingRace) if v.value >= 15]

strategySchema = pd.DataFrame(np.zeros(shape=(12, 18)), index=SWIMMERS, columns=allEvents)
scoreSchema = ScoreSchema()
print(scoreSchema.schema)
print(scoreSchema.timeSchema)

# PROBLEM
model = pulp.LpProblem('Swimming score maximizing problem', pulp.LpMaximize)

# creating all the variables
swimmerStatus = pulp.LpVariable.dicts('swimmerStatus',
                                     ((swimmer, event) for swimmer in SWIMMERS for event in allEvents), cat='Binary')
numberOfRelays = pulp.LpVariable('numberOfRelays', lowBound=1, upBound=2, cat=pulp.LpInteger)

# COST FUNCTION
model += pulp.lpSum([swimmerStatus[(s, e)] * scoreSchema.schema.loc[s, e]
                    for e in allEvents for s in SWIMMERS])

# CONSTRAINTS
for swimmer in SWIMMERS:
    # individual constraint1: where the sum of a swimmer's individual events must not exceed 4
    model += pulp.lpSum([swimmerStatus[(swimmer, e)] for e in individualEvents]) <= 4
    # individual constraint2: where the sum of a swimmer's individual+relay events must not exceed 5
    model += pulp.lpSum([swimmerStatus[(swimmer, e)] for e in allEvents]) <= 5
    # relay constraint3: you cannot be in the IMRelay4P50 more than 1 time.
    model += pulp.lpSum([swimmerStatus[(swimmer, e)] for e in IMrelay]) <= 1

for e in individualEvents:
    # team constraint1: where the amount of swimmers per individual event per team must not exceed 4
    model += pulp.lpSum([swimmerStatus[(swimmer, e)] for swimmer in SWIMMERS]) <= 4


# relay constraint1: there must be 4 or 8 people in each FRRelay4P50, and FRRelay4P100
model += pulp.lpSum([swimmerStatus[(swimmer, 'FRRelay4P50')] for swimmer in SWIMMERS]) == 4 * numberOfRelays
model += pulp.lpSum([swimmerStatus[(swimmer, 'FRRelay4P100')] for swimmer in SWIMMERS]) == 4 * numberOfRelays
# relay constraint2: there must be 4 people for IMRelay4P50
model += pulp.lpSum([swimmerStatus[(s, e)] for e in IMrelay for s in SWIMMERS]) == 4 * numberOfRelays
# relay constraint4: IMRelay4P50 must be 4 people swimming different strokes
for stroke in IMrelay:
    model += pulp.lpSum([swimmerStatus[(s, stroke)] for s in SWIMMERS]) <= numberOfRelays


# SOVLE
model.solve()
print(pulp.LpStatus[model.status])
# display results
output = []
for swimmer in SWIMMERS:
    row = []
    for s, e in swimmerStatus:
        if swimmer == s:
            row.append(swimmerStatus[(s, e)].varValue)
        else: 
            continue
    output.append(row)


OUTPUTDF = pd.DataFrame(output, index=SWIMMERS, columns=allEvents)
print(OUTPUTDF)
print(pulp.value(model.objective))
OUTPUTDF.to_excel('data/schema.xlsx', sheet_name='bois_schema')
