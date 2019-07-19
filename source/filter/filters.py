import pandas as pd
from source.settings import SwimmingRace, SKILL_SET
import os


def assess_skill(df, swimmer, race_name):
    """
    Finds the skills for missing events that the swimmer does not have.
    """
    races = df[(df['Event'] == race_name) & (df['Name'] == swimmer)]
    if len(races) == 0:
        all_skill_names = [v.name for v in SKILL_SET.keys()]
        matching_race = SKILL_SET[SwimmingRace[race_name]] if race_name in all_skill_names else None
        # Find skill set of a race that the swimmer does not have any times for.
        if matching_race is None:
            return race_name, 'NT'
        else: 
            return df[(df['Event'] == matching_race.name) & (df['Name'] == swimmer)]
        
    else:
        return races 


def time_min(df, swimmer, race_name):
    """
    Finds the fastest time that swimmer `swimmer` has in `race_name`.
    """
    races = assess_skill(df, swimmer, race_name)
    min_race = races.loc[races['Time'].idxmin()]
    return min_race['Event'], min_race['Time']


def time_max(df, swimmer, race_name):
    """
    Finds the slowest time that swimmer `swimmer` has in `race_name`.
    """
    races = assess_skill(df, swimmer, race_name)
    max_race = races.loc[races['Time'].idxmax()]
    return max_race['Event'], max_race['Time']


def time_mean(df, swimmer, race_name):
    """
    Finds the average time that swimmer `swimmer` has in `race_name`.
    """
    races = assess_skill(df, swimmer, race_name)
    mean_time = races['Time'].mean()
    return races['Event'].iloc[0], round(mean_time, 2)

