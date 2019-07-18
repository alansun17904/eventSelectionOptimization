from .context import *
import datetime
import pandas as pd
import pytest


@pytest.fixture(scope='module')
def load_swimmer_data():
    os.chdir('data/in/')
    original_data = pd.read_excel('processed.xlsx', sheet_name='Sheet1')  # read in excel sheet with all historic data
    original_data['Time'] = original_data['Time'].apply(models.Schema.timeConversion)  # convert fields `time` to datetime objects
    original_data['Date'] = pd.to_datetime(original_data['Date'])
    return original_data


@pytest.fixture(scope='module')
def load_comparison_db(load_swimmer_data):
    return filter.create_comparison_db(load_swimmer_data, filter.time_min)


def test_create_comparison_db(load_swimmer_data):
    df = filter.create_comparison_db(load_swimmer_data, filter.time_max)
    assert len(df) == 1988
    assert len(filter.assess_skill(load_swimmer_data, 'Alan Sun', 'FR50m')) == 38
    assert len(filter.assess_skill(load_swimmer_data, 'Miles Huang', 'FR50m')) == 12
    assert len(filter.assess_skill(load_swimmer_data, 'Kan KikuchiYuan', 'IM200m')) == 14
    assert len(filter.assess_skill(load_swimmer_data, 'Aaron Sun', 'FLY100m')) == 15


def test_score_max_internal_db(load_swimmer_data):
    df = filter.create_comparison_db(load_swimmer_data, filter.time_min)
    assert filter.score_max_internal_db(load_swimmer_data, df, 'Alan Sun', 'FR50m') == 16


def test_score_min_internal_db(load_swimmer_data):
    df = filter.create_comparison_db(load_swimmer_data, filter.time_min)
    assert filter.score_min_internal_db(load_swimmer_data, df, 'Alan Sun', 'FR50m') == 0
    assert filter.score_min_internal_db(load_swimmer_data, df, 'Miles Huang', 'FR100m') == 0
    assert filter.score_min_internal_db(load_swimmer_data, df, 'Aaron Sun', 'FR50m') == 0
    assert filter.score_min_internal_db(load_swimmer_data, df, 'Joseph Chew', 'BR50m') == 0


def test_score_weighted_average_internal_db(load_swimmer_data):
    df = filter.create_comparison_db(load_swimmer_data, filter.time_min)
    print(filter.score_weighted_average_internal_db(load_swimmer_data, df, 'Alan Sun',
                                                          'FR50m', datetime.datetime(2000, 1, 1),
                                                          datetime.datetime(2020, 1, 1)))
    assert type(filter.score_weighted_average_internal_db(load_swimmer_data, df, 'Alan Sun',
                                                          'FR50m', datetime.datetime(2000, 1, 1),
                                                          datetime.datetime(2020, 1, 1))) == float


