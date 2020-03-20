import math

spring_calc = {
'magi' : 5,
'nobles' : 5,
'companions' : 3,
'crafters' : 2,
'specialists': 2,
}

class Covenant:
    def __init__(self):
        self.covenant_season = 'spring'
        self.income_sources = {}
        self.covenfolk_tiers = {
            'magi' : 6,
            'nobles' : 0,
            'companions' : 4,
            'crafters' : 0,
            'specialists': 3,
            'dependants': 0,
            'grogs': 10,
            'laborers' : 0,
            'servants' : 12,
            'teamsters' : 7,
            'horses': 0
            }
        self.covenfolk_points = 0
        self.expenditures = {}

    def calculate_points(self):
        point_cost = 0
        if self.covenant_season == 'spring' or self.covenant_season == 'summer':
            for k, v in self.covenfolk_tiers.items():
                point_cost += spring_calc.get(k, 1) * v
            #math for calculating
            return point_cost
        else:
            # math for calculating
            pass

    def calc_servants(self):
        cov_for_servants = ['magi', 'nobles', 'companions', 'crafters', 'specialists', 'dependants', 'grogs', 'horses']
        points = 0
        if self.covenant_season == 'spring':
            for cov in cov_for_servants:
                points += spring_calc.get(cov, 1) * self.covenfolk_tiers[cov]
        return 2 * math.ceil(points / 10)

    def calc_expenditures(self):
        expend = {}
        expend['buildings'] = math.ceil(self.calculate_points() / 10)
        expend['consumables'] = 2 * math.ceil(self.calculate_points() / 10)
        expend['inflation'] = 0
        expend['laboratories'] = 0
        expend['provisions'] = 5 * math.ceil(self.calculate_points() / 10)
        expend['tithes'] = 0
        expend['wages'] = 2 * math.ceil(self.calculate_points() / 10)
        return expend
    
cov = Covenant()
print(cov.calculate_points())
print(cov.calc_servants())
print(cov.calc_expenditures())
