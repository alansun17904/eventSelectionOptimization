from source import filter
from source import lp
from datetime import datetime
from source import settings
from source import models
from source.filter.filters import time_min
from source.filter.scoring import score_min_internal_db
from source.simulation.compare_apac import Simulation


schema = models.Schema(swimmers=settings.SWIMMERS, allevents=settings.SwimmingRace,
                       limitdate=datetime(2018, 1, 20), filterF=time_min,
                       score_func=score_min_internal_db)
events = [e.name for e in settings.SwimmingRace]
individual_events = [e.name for e in settings.SwimmingRace if e.value < 13]
relay_events = [e.name for e in settings.SwimmingRace if e.name not in individual_events]
im_relay = [e.name for e in settings.SwimmingRace if e.value >= 15]
optimize = lp.Optimize(settings.SWIMMERS, events=events, min_relays=1,
                      max_relays=2, score=schema, ind_events=4, ind_relay_events=5,
                      individualEvents=individual_events, IMrelay=im_relay,
                      team_num=4)
optimize.optimize()
# optimize.write_optimal()
s = Simulation(2018, optimize)
apac_df = s.run_simulation()
print(s.score_apac())
# print(apac_df[(apac_df['Event'] == 'FR100m') & (apac_df['Prelim/Finals'] != 'Prelim')]
#       [['SchoolSerial', 'Name', 'Time', 'Rank', 'Event', 'Prelim/Finals']])
