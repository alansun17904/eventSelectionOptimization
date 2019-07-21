from source.lp.optimize import Optimize
from source.models.schema import Schema
import pandas as pd


class Simulation:
    def __init__(self, year, optimize: Optimize):
        """
        :param year: (int) APAC year that is being compared to.
        :param optimize: optimize object that contains the optimal solution
        """
        if 'optimal' not in dir(optimize):
            optimize.optimize()
        self.optimal_solution = optimize.optimal
        self.year = year

    def read_apac_data(self):
        original_data = pd.read_excel('data/in/APAC_all.xlsx', sheet_name='Sheet1')
        original_data['Time'].apply(Schema.timeConversion)
        original_data['Date'].apply(lambda s: int(str(s)[0:4]))
        original_data = original_data[original_data['Date'] == self.year]

    def
