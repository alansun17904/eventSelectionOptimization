import source.filter.filters as filters
import source.settings as settings
import pandas as pd
import math
import datetime as dt


def create_comparison_db(df, filterF):
    unique_db = {'Name': [],
                 'Gender': [],
                 'Event': [],
                 'Time': []}
    for name in df['Name'].unique():
        for event in df[df['Name'] == name]['Event'].unique():
            unique_db['Name'].append(name)
            unique_db['Gender'].append(df[df['Name'] == name]['Gender'].iloc[0])
            unique_db['Event'].append(event)
            unique_db['Time'].append(filterF(df, name, event)[1])
    return pd.DataFrame(unique_db)


def score_max_internal_db(whole_df, comparison_df, swimmer, race_name):
    """
    Filters each swimmer's in the entire database using the `time_min` function. 
    The target swimmers time is then compared within this new model and a rank is 
    derived from this using the SCORE map from settings. Calculates the maxmium number
    of points the swimmer would score by chosing to score their fastest time.
    :returns: a float that represents the score that target swimmer gets in ranking system.
    """
    self_races = filters.time_min(whole_df, swimmer, race_name)  # TODO: change filters.time_min to take from settings.py
    races = comparison_df[(comparison_df['Event'] == race_name) &  # check if event is the same
                          (comparison_df['Gender'] == settings.GENDER) &
                          (comparison_df['Name'] != swimmer) &  # target swimmer does not compare against themselves
                          (comparison_df['Time'] < self_races[1])]  # how many swimmers are faster than target
    return settings.score(len(races) + 1)


def score_min_internal_db(whole_df, comparison_df, swimmer, race_name):
    """
    Filters each swimmer's in the entire database using the `time_max` function.
    The target swimmers time is then compared within this new model and a rank is
    derived from this using the SCORE map from settings.
    :param whole_df: The entire dataframe with all data in the database
    :param comparison_df: The dataframe that is being used for comparison
    :param swimmer: (str) name of the swimmer
    :param race_name: (str) event name, in serial form can be found in the `SwimmingRace` class
    :return: float -> score
    """
    gender = 'BOYS'
    self_races = filters.time_max(whole_df, swimmer, race_name)
    races = comparison_df[(comparison_df['Event'] == race_name) &  # check if event is the same
                          (comparison_df['Gender'] == settings.GENDER) &
                          (comparison_df['Name'] != swimmer) &  # target swimmer does not compare against themselves
                          (comparison_df['Time'] < self_races[1])]  # how many swimmers are faster than target
    return settings.score(len(races) + 1)


def score_weighted_average_internal_db(whole_df, comparison_df, swimmer, race_name, startdate, enddate):
    # TODO: Finish this score function
    """
    Scores swimmers based on a weighted average. The closer the date is to the enddate / today the more meaningful
    their point contributions will be.
    :param whole_df:  The entire dataframe with all data from database.
    :param comparison_df: A dataframe with unique entries for events + swimmer names that is used for comparison
    :param swimmer: (str) The name of the swimmer
    :param race_name: (str) The event name, in serial form that can be found in the `SwimmingRace` class
    :param startdate: (datetime) Marking the startdate for all swims that are being averaged
    :param enddate: Marking the enddate for all swims that can be averaged.
    :return: float -> score
    """
    self_races = filters.assess_skill(whole_df, swimmer, race_name)
    self_races = self_races[self_races['Date'].between(startdate, enddate)]  # limiting to rows that are between dates
    total_scores = []
    for index, race in self_races.iterrows():
        rank = comparison_df[(comparison_df['Event'] == race_name) &
                             (comparison_df['Gender'] == settings.GENDER) &
                             (comparison_df['Name'] != swimmer) &
                             (comparison_df['Time'] < race['Time'])]
        delta_days = (enddate - dt.datetime(race['Date'].year, race['Date'].month, race['Date'].day)).days
        score = settings.score(len(rank))
        total_scores.append((score * (1 / delta_days), 1 / delta_days))
    # return sum(v[0] for v in total_scores]) / sum([v[1] for v in total_scores])


def score_past_apac(df, swimmer, race_name, startdate, enddate, prelims=True):
    """
    Compares target swimmer's times with APAC database. Specific APAC
    configurations can be changed with `date` and `prelims`.
    startdate (datetime obj.): the date that
    enddate(datetime obj.): the date that
    """
    pass
