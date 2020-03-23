import math

spring_calc = {
'magi' : 5,
'nobles' : 5,
'companions' : 3,
'crafters' : 2,
'specialists': 2,
}
cost_max = {
    'buildings' : 0.5,
    'consumables' : 0.2,
    'laboratories' : 0.2,
    'provisions' : 0.2,
    'arms' : 0.5,
    'writing' : 0.5}

class Covenant:
    def __init__(self):
        self.covenant_season = 'spring'
        self.income_sources = {'agriculture' : 100}
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
        self.covenfolk_points = self.calc_points()
        self.expenditures = self.calc_expenditures()
        self.treasury = 50.0

    def calc_points(self):
        point_cost = 0
        if self.covenant_season == 'spring' or self.covenant_season == 'summer':
            for k, v in self.covenfolk_tiers.items():
                point_cost += spring_calc.get(k, 1) * v
            #math for calculating
            return point_cost
        else:
            # math for calculating Fall or Winter covenants
            pass

    def calc_needs(self):
        cov_for_servants = ['magi', 'nobles', 'companions', 'crafters', 'specialists', 'dependants', 'grogs', 'horses']
        points = 0
        if self.covenant_season == 'spring':
            for cov in cov_for_servants:
                points += spring_calc.get(cov, 1) * self.covenfolk_tiers[cov]
        needs = [math.ceil(points / 10) * 2, math.ceil(points / 10) - (2 * self.covenfolk_tiers['laborers'])]
        return needs
    
    def calc_expenditures(self):
        expend = {}
        expend['buildings'] = self.calc_points() / 10
        expend['consumables'] = 2 * (self.calc_points() / 10)
        expend['inflation'] = 0
        expend['laboratories'] = 0
        expend['provisions'] = 5 * (self.calc_points() / 10)
        expend['tithes'] = 0
        expend['wages'] = 2 * (self.calc_points() / 10)
        return expend
    
    def total_expenditure(self):
        total = 0
        for val in self.calc_expenditures().values():
            total += val
        return total
    def total_income(self):
        total = 0
        for val in self.income_sources.values():
            total += val
        return total

    def display_finances(self):
        for key, val in self.calc_expenditures().items():
            print(key.ljust(15) + str(val).rjust(8))
        print ('Total:'.ljust(15) + str(self.total_expenditure()).rjust(8))
        print('\nTotal income:' + str(self.total_income()).rjust(10))
        print('Treasury:' + str(self.treasury).rjust(14))
    
cov = Covenant()
print('Total covenant points: %s' % cov.calc_points())
print('Needed servants and teamsters: %s' % cov.calc_needs())
cov.display_finances()
