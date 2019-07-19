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
    1:  16,
    2:  13,
    3:  12,
    4:  11,
    5:  10,
    6:  9,
    7:  7,
    8:  5,
    9:  4,
    10: 3,
    11: 2,
    12: 1,
}

SWIMMERS = ['Miles Huang', 'Curtis Wong', 'King Wah', 'Justin Choi', 'Aaron Wu', 'Frank Zhou',
            'Alan Wang', 'Alan Sun', 'Bernard Ip', 'Kan KikuchiYuan', 'Jerry Zheng', 'Aaron Sun']

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
    if rank > 12:
        return 0
    else:
        return SCORE[rank]