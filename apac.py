from datetime import datetime
import pandas as pd


class APAC:
    def __init__(self, gender="BOYS", year=None, prelims=0):
        """

        :param gender:
        :param year:
        :param prelims:
            0: denotes that all prelims and finals should be considered
            1: only prelims
            2: only finals
        """
        self.APAC_data = pd.read_excel('data/APAC_all.xlsx', sheet_name='Sheet1')
        self.APAC_data['Date'] = self.APAC_data['Date'].apply(lambda s: datetime.strptime(str(s), '%Y%m%d'))

        if year is not None:
            print("You are comparing against all of " + str(year) + "'s swims.")
            self.APAC_data = self.APAC_data[self.APAC_data['Date'].year == year]
        self.APAC_data['Time'] = self.APAC_data['Time'].apply(APAC.time_conversion)
        self.APAC_data = self.APAC_data[self.APAC_data['Gender'] == gender]

        if prelims == 1:
            self.APAC_data = self.APAC_data[self.APAC_data['Prelim/Finals'] == 'Prelim']
        elif prelims == 2:
            self.APAC_data = self.APAC_data[self.APAC_data['Prelim/Finals'] == 'Finals']

    def compare(self, event, time):
        inevent = self.APAC_data[self.APAC_data['Event'] == event]
        rank = inevent[inevent['Time'] < time].shape[0] + 1
        return rank

    @staticmethod
    def time_conversion(time):
        if type(time) == str and len(time.split('.')) == 2:
            return float(time)
        if type(time) == float or type(time) == int:
            return float(time)
        s = time.split('.')
        return float(s[0])*60 + float('.'.join(s[1:]))

