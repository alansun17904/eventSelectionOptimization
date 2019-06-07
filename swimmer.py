import enum
import apac

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

SCORE_8LANE = {
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
    16: 1
}

SWIMMERS = ['Miles Huang', 'Curtis Wong', 'King Wah', 'Justin Choi', 'Aaron Wu', 'Frank Zhou',
            'Alan Wang', 'Alan Sun', 'Bernard Ip', 'Kan KikuchiYuan', 'Jerry Zheng', 'Aaron Sun']


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


class Filter:
    ranksuite = apac.APAC(year=2017, prelims=0)  # FIXME: This is not good architecture....
    skillFinder = {'FRRelay4P50': 'FR50m',
                   'FRRelay4P100': 'FR100m',
                   'IMRelay4P50_FR': 'FR50m',
                   'IMRelay4P50_BR': 'BR50m',
                   'IMRelay4P50_BA': 'BA50m',
                   'IMRelay4P50_FLY': 'FLY50m'}

    @staticmethod
    def rank(place):
        # this needs to be changed based on the number of lanes in the pool
        # as well as the configuration of the finals.
        if place <= 12:
            return SCORE[place]
        else:
            return 0

    @staticmethod
    def takeMax(df, name, event):
        """
        df: DataFrame that contains all of the swimmer's data.
        name: The name of the swimmer that is being scored.
        event: The corresponding event taht is being score.
        This function compiles the data from the swimming table together and
        outputs a list with the name of the event and the swimmers score in that event.
        It calculates the score using the maximum function, considering all of
        the swims and taking the best one.
        :return: [event (str), score (int), time (float)]
        """
        racesForTargetSwimmer = df[(df['Event'] == event) & (df['Name'] == name)]
        if len(racesForTargetSwimmer) == 0:  # Relay event
            points, time = Filter.assessSkill(df, name, event)
            return [event, points, time]
        else:
            if len(racesForTargetSwimmer) == 1:
                time = racesForTargetSwimmer.iloc[0]['Time']
                place = Filter.ranksuite.compare(event, time)
                return [event, Filter.rank(place), time]
            else:
                minimum = racesForTargetSwimmer.loc[racesForTargetSwimmer['Time'].idxmin()]
                # COST FUNCTION RIGHT HERE
                time = minimum.loc['Time']
                place = Filter.ranksuite.compare(event, time)
                if place == 0:  # Relay event if the swimmer has swam a relay event before
                    p, time = Filter.assessSkill(df, name, event)
                    return [event, p, time]
                return [event, Filter.rank(place), time]
    
    @staticmethod
    def takeAverage(df, name, event):
        pass
    
    @staticmethod
    def takeMin(df, name, event):
        pass
    
    @staticmethod
    def takeRecent(df, name, event):
        pass

    @staticmethod
    def assessSkill(df, name, event):
        """
        event (str): the name of the event that does not have a rank.
        If you have an individual time for the FR50 or the FR100 and never 
        swam in a relay before your point contribution to that relay would be 
        you score in that event / 2. If you have a time in one of the 50IMs that could 
        also be used when you are being seeded into the IMRelay.

        Rankings in relays cannot be converted and used as individual time. 
        :returns: the amount of points that the swimmer would get in that event based on their skills.
        If they do not have that skill then a large negative number is used to denote the large risk / cost
        putting that swimmer in this event implies.
        """
        if event in Filter.skillFinder.keys():
            skill = Filter.skillFinder[event]
            swimmerEvent = df[(df['Event'] == skill) & (df['Name'] == name)]
            time = swimmerEvent['Time'].iloc[0]
            if swimmerEvent.shape[0] == 0:
                # if the person does not possess this event and also does not have the skill
                return -1000, 'NT'
            place = Filter.ranksuite.compare(skill, time)
            return Filter.rank(place) / 4, time
        else:
            return -1000, 'NT'


if __name__ == '__main__':
    print(Filter.assessSkill(0, 0, 0))
