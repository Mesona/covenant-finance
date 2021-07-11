import math
from covenfolk import Covenfolken

covenant_season_costs = {
        "spring": {
            "magi": 5,
            "nobles": 5,
            "companions": 3,
            "crafters": 2,
            "specialists": 2,
            "covenfolk": 1,
            "horse": 1,
        },
        "summer": {
            "magi": 10,
            "nobles": 10,
            "companions": 5,
            "crafters": 3,
            "specialists": 3,
            "covenfolk": 2,
            "horse": 1,
        },
        "fall": {
            "magi": 5,
            "nobles": 5,
            "companions": 3,
            "crafters": 2,
            "specialists": 2,
            "covenfolk": 2,
            "horse": 1,
        },
        "winter": {
            "magi": 5,
            "nobles": 5,
            "companions": 3,
            "crafters": 2,
            "specialists": 2,
            "covenfolk": 1,
            "horse": 1,
        },
}

maximum_cost_savings = {
    "buildings" : 0.5,
    "consumables" : 0.2,
    "laboratories" : 0.2,
    "provisions" : 0.2,
    "arms" : 0.5,
    "writing" : 0.5,
}

class Covenant:
    def __init__(
            self,
            name = "Vernus",
            season = "spring",
            income_sources = {"source": 100},
            tithes = {},
            treasury = 50.0,
            covenfolken = Covenfolken(),
            laboratories = {},
            armory = 0,
            inflation_enabled = True,
            inflation_value = 0,
        ):
        self.name = name

        if season.lower() in ["spring", "summer", "winter", "fall"]:
            self.season = season.lower()
        else:
            raise ValueError(f"""
Season {season} is not an accepted covenant season!
Please select between spring, summer, fall, and winter.
""")
        for k, v in income_sources.items():
            if not isinstance(k, str):
                raise TypeError("Income source names need to be strings!")
            if not isinstance(v * 1.0, float):
                raise TypeError("Income source values need to be numbers!")

        self.income_sources = income_sources
        self.tithes = tithes
        self.treasury = treasury
        self.covenfolken = Covenfolken()
        self.laboratories = laboratories
        self.armory = armory
        self.treasury = treasury
        self.inflation_enabled = inflation_enabled
        self.inflation = inflation_value
        self.expenses = float("inf")  # Prevents inflation from taking effect the first year
            
    def calc_covenfolk_points(self):
        point_cost = 0
        for covenfolk in self.covenfolken.covenfolk.values():
            point_cost += covenant_season_costs[self.season][covenfolk.classification]
        return point_cost

    def calc_servant_minimum(self):
        covenfolk_roles = ["magi", "nobles", "companions", "crafters", "specialists", "dependants", "grogs", "horses"]
        covenfolk_points = 0

        for covenfolk in covenfolk_roles:
            covenfolk_points += covenant_season_costs[self.season][covenfolk] * self.covenfolken[covenfolk]

        servant_minimums = math.ceil(points / 10) * 2
        return servant_minimums

    def calc_teamster_minimum(self):
        covenfolk_roles = ["magi", "nobles", "companions", "crafters", "specialists", "dependants", "grogs", "horses", "servants"]
        covenfolk_points = 0

        for covenfolk in covenfolk_roles:
            covenfolk_points += covenant_season_costs[self.season][covenfolk] * self.covenfolken[covenfolk]

        teamster_minimums = math.ceil(points / 10)
        return teamster_minimums
    
    def calc_expenditures(self):
        expend = {}
        expend['buildings'] = self.calc_covenfolk_points() / 10
        expend['consumables'] = 2 * (self.calc_covenfolk_points() / 10)
        expend['laboratories'] = self.calc_lab_points() / 10
        expend['provisions'] = 5 * (self.calc_covenfolk_points() / 10)
        expend['armory'] = self.armory / 320
        expend['tithes'] = sum(self.tithes.values())
        expend['wages'] = 2 * (self.calc_covenfolk_points() / 10)
        expend['writing'] = self.covenfolken.total("writer") + self.covenfolken.total("magi")

        savings = self.calc_savings(expend)
        ##TODO: factor in savings

        expenses = sum(expend.values())

        previous_years_expenses = self.expenses
        self.expenses = expenses
        if self.inflation_enabled:
            inflation = self.calculate_inflation(previous_years_expenses)
            self.inflation = inflation



    def calculate_inflation(self, previous_expenses):
        # Page 65 of Covenant book, inflation should only increase if the year's
        # expenditures were greater than the previous year's
        if self.expenses - previous_expenses > 0:
            inflation = expenses // 100

        return inflation

    # I need to figure out how to do this
    # list comprehension on cost_savings?
    def calc_savings(self, category):
        #app_craft = [crafter for crafter in self.cost_savings if crafter[0] == category]
        #return app_craft
        pass
    
    def calc_lab_points(self):
        points = 0
        for lab in self.laboratories:
            points += lab.points
        return points
    
    def total_expenditure(self):
        return self.expenses
                   
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

    def advance_year(self):
        self.treasury = self.treasury + self.total_income() - self.total_expenditure()
