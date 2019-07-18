from .context import *
import os
import pytest
import pandas as pd


@pytest.fixture(scope='module')
def load_swimmer_data():
    os.chdir('data/in/')
    originalData = pd.read_excel('processed.xlsx', sheet_name='Sheet1')  # read in excel sheet with all historic data
    originalData['Time'] = originalData['Time'].apply(models.Schema.timeConversion)  # convert fields `time` to datetime objects
    originalData['Date'] = pd.to_datetime(originalData['Date'])
    return originalData


def test_assess_skill(load_swimmer_data):
    t1 = filter.assess_skill(load_swimmer_data, 0, 0)
    assert t1 is not None
    assert len(t1) == 2

    t2 = filter.assess_skill(load_swimmer_data, 'Alan Wang', settings.SwimmingRace(13).name)
    assert t2 is not None
    assert len(t2) == 25


def test_time_min(load_swimmer_data):
    t1 = filter.time_min(load_swimmer_data, 'Alan Sun', settings.SwimmingRace(1).name)
    print(t1)
    assert t1 is not None
    assert t1[0] == settings.SwimmingRace(1).name
    assert t1[1] == 24.01

    t2 = filter.time_min(load_swimmer_data, 'Joseph Chew', settings.SwimmingRace(6).name)
    assert t2 is not None
    assert t2[0] == settings.SwimmingRace(6).name
    assert t2[1] == 66.65

    t3 = filter.time_min(load_swimmer_data, 'Bernard Ip', settings.SwimmingRace(13).name)
    assert t3 is not None
    assert t3[0] == settings.SwimmingRace(1).name
    assert t3[1] == 25.46


def test_time_max(load_swimmer_data):
    t1 = filter.time_max(load_swimmer_data, 'Alan Sun', settings.SwimmingRace(1).name)
    assert t1 is not None
    assert t1[0] == settings.SwimmingRace(1).name
    assert t1[1] == 33.18

    t2 = filter.time_max(load_swimmer_data, 'Miles Huang', settings.SwimmingRace(8).name)
    assert t2 is not None
    assert t2[0] == settings.SwimmingRace(8).name
    assert t2[1] == 38.21

    t3 = filter.time_max(load_swimmer_data, 'Alan Wang', settings.SwimmingRace(18).name)
    assert t3 is not None
    assert t3[0] == settings.SwimmingRace(9).name
    assert t3[1] == 35.15


def test_time_mean(load_swimmer_data):
    t1 = filter.time_mean(load_swimmer_data, 'Alan Sun', settings.SwimmingRace(1).name)
    assert t1 is not None
    assert t1[0] == settings.SwimmingRace(1).name
    assert t1[1] == 26.28
