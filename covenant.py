import math
import covenant_constants as cc
# Constants, pulled from the book.

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
##        self.covenfolk_points = self.calc_points()
##        self.expenditures = self.calc_expenditures()
        self.laboratories = {
            'Bonny' : 0,
            'Merry' : 0,
            'Tremmy' : 0,
            'Jerry' : 0,
            'Guenny' : 0,
            'Ex Max' : 0}
        self.treasury = 50.0

    def calc_points(self):
        point_cost = 0
        if self.covenant_season == 'spring' or self.covenant_season == 'winter':
            default = 1
        else:
            default = 2
        for k, v in self.covenfolk_tiers.items():
            point_cost += cc.spring_calc.get(k, 1) * v
        return point_cost

    def calc_needs(self):
        cov_for_servants = ['magi', 'nobles', 'companions', 'crafters', 'specialists', 'dependants', 'grogs', 'horses']
        points = 0
        if self.covenant_season == 'spring':
            for cov in cov_for_servants:
                points += cc.spring_calc.get(cov, 1) * self.covenfolk_tiers[cov]
        needs = [math.ceil(points / 10) * 2, math.ceil(points / 10) - (2 * self.covenfolk_tiers['laborers'])]
        return needs
    
    def calc_expenditures(self):
        expend = {}
        expend['buildings'] = self.calc_points() / 10
        expend['consumables'] = 2 * (self.calc_points() / 10)
        expend['inflation'] = 0
        expend['laboratories'] = self.calc_labs() / 10
        expend['provisions'] = 5 * (self.calc_points() / 10)
        expend['armory'] = 0
        expend['tithes'] = 0
        expend['wages'] = 2 * (self.calc_points() / 10)
        expend['writing']= 0
        return expend
    
    def calc_labs(self):
        total = 0
        for key, val in self.laboratories.items():
            total += cc.lab_upkeep(val)
        return total
        
    def total_expenditure(self):
        return sum(self.calc_expenditures().values())
                   
    def total_income(self):
        return sum(self.income_sources.values())

    def display_finances(self):
        for key, val in self.calc_expenditures().items():
            print(key.ljust(15) + str(val).rjust(8))
        print ('Total:'.ljust(15) + str(self.total_expenditure()).rjust(8))
        print('\nTotal income:' + str(self.total_income()).rjust(10))
        print('Treasury:' + str(self.treasury).rjust(14))
        #print()

    def display_labs(self):
        print('Name:'.ljust(15) + 'Upkeep'.rjust(8))
        for key, val in self.laboratories.items():
            print(key.ljust(20) + str(val).rjust(3))
        #print()
    
    def bank(self, silver):
        self.treasury += silver

