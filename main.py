from source import filter
from source import lp
from datetime import datetime
from source import settings
from source import models
from source.settings import SCORE_FUNCTION


schema = models.Schema(swimmers=settings.SWIMMERS, limitdate=datetime(2020, 1, 1), filterF=settings.FILTER_FUNCTION,
                       score=SCORE_FUNCTION)
events = [e.name for e in settings.SwimmingRace]
individual_events = [e.name for e in settings.SwimmingRace if e.value < 13]
relay_events = [e.name for e in settings.SwimmingRace if e.name not in individual_events]
optimze = lp.Optimize(settings.SWIMMERS, events=events, min_relays=1,
                      max_relays=2, score=schema.schema, ind_events=4, ind_relay_events=5,
                      individualEvens=individual_events, IMrelay=['FR50m', 'FLY50m', 'BA50m', 'BR50m'],
                      team_num=4)
print(optimze.optimize())