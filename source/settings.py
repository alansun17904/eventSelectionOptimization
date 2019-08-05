import enum
import os


@enum.unique
class SwimmingRace(enum.Enum):
    FR50m = 1
    FR100m = 2
    FR200m = 3
    FR400m = 4
    BR50m = 5
    BR100m = 6
    BA100m = 7
    BA50m = 8
    FLY50m = 9
    FLY100m = 10
    IM100m = 11
    IM200m = 12
    FRRelay4P50 = 13
    FRRelay4P100 = 14
    IMRelay4P50_FR = 15
    IMRelay4P50_BR = 16
    IMRelay4P50_BA = 17
    IMRelay4P50_FLY = 18


SCORE = {
    0:  30,  # TODO: This is a temporary fix for to avoid implementing a cost function
    1:  20,
    2:  17,
    3:  16,
    4:  15,
    5:  14,
    6:  13,
    7:  12,
    8:  11,
    9:  9,
    10: 7,
    11: 6,
    12: 5,
    13: 4,
    14: 3,
    15: 2,
    16: 1,
}

SWIMMERS = ['Kan KikuchiYuan', 'Alan Wang', 'Aaron Wu', 'Kingston Yip', 'Matthew Yu', 'Aaron Sun',
            'Justin Choi', 'Curtis Wong', 'Sung Cho', 'Alan Sun', 'Joseph Chew', 'Harry Shiu']

GENDER = 'BOYS'

SKILL_SET = {
    SwimmingRace(13): SwimmingRace(1),
    SwimmingRace(14): SwimmingRace(2),
    SwimmingRace(15): SwimmingRace(2),
    SwimmingRace(16): SwimmingRace(5),
    SwimmingRace(17): SwimmingRace(8),
    SwimmingRace(18): SwimmingRace(9),
}

# FILTER_FUNCTION = time_min
#
# SCORE_FUNCTION = score_max_internal_db


def score(rank):
    if rank > 16:
        return 0
    else:
        return SCORE[rank]