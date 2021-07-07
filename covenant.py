import math

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
    "writing" : 0.5}
}

class Covenant:
    def __init__(
            self,
            name = "Vernus",
            season = "spring",
            income_sources = {"source": 100},
            tithes = {},
            treasury = 50.0,
            writers = 0,
            cost_savings = [],
            covenfolk_tiers = {},
            laboratories = {},
            armory = "",
            inflation_enabled = True,
            inflation_value = 0,
            minor_fortifications = 0,
            major_foritifications = 0,
        ):
        self.name = name

        if season.lower() in ["spring", "summer", "winter", "fall"]:
            self.season = season.lower()
        else:
            raise ValueError(f"
Season {season} is not an accepted covenant season!
Please select between spring, summer, fall, and winter.
")
        for k, v in income_sources.items():
            assert isinstance(k, str)
            assert isinstance(v * 1.0, float)

        self.income_sources = income_sources
        self.treasury = treasury
        self.writers = writers
        self.cost_savings = cost_savings
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
        self.laboratories = laboratories
        if armory == "":
            self.armory = self.covenfolk_tiers['grogs'] * 32
        else:
            self.armory = armory
        self.treasury = 50.0
        self.armory = self.covenfolk_tiers['grogs'] * 32
        self.writers = 0
        self.cost_savings = []
        self.inflation_enabled = inflation_enabled
        self.inflation = inflation_value
        self.minor_foritifications = minor_fortifications + sum(lab.minor_fortifications for lab in self.laboratories)
        self.major_foritifications = major_foritifcations + sum(lab.major_fortifications for lab in self.laboratories)
        self.expenses = self.calc_expenditures()
            
    def calc_covenfolk_points(self):
        point_cost = 0
        # FIXME: What are these lines intended to do?
        #if self.season == "spring" or self.season == "winter":
        #    default = 1
        #else:
        #    default = 2
        for covenfolk, amount in self.covenfolk_tiers.items():
            point_cost += covenant_season_costs[self.season][covenfolk] * amount
        return point_cost

    def calc_servant_minimum(self):
        covenfolk_roles = ["magi", "nobles", "companions", "crafters", "specialists", "dependants", "grogs", "horses"]
        covenfolk_points = 0

        for covenfolk in covenfolk_roles:
            covenfolk_points += covenant_season_costs[self.season][covenfolk] * self.covenfolk_tiers[covenfolk]

        servant_minimums = math.ceil(points / 10) * 2
        return servant_minimums

    def calc_teamster_minimum(self):
        covenfolk_roles = ["magi", "nobles", "companions", "crafters", "specialists", "dependants", "grogs", "horses", "servants"]
        covenfolk_points = 0

        for covenfolk in covenfolk_roles:
            covenfolk_points += covenant_season_costs[self.season][covenfolk] * self.covenfolk_tiers[covenfolk]

        teamster_minimums = math.ceil(points / 10)
        return teamster_minimums
    
    def calc_expenditures(self):
        expend = {}
        expend['buildings'] = self.calc_covenfolk_points() / 10
        expend['consumables'] = 2 * (self.calc_covenfolk_points() / 10)
        expend['laboratories'] = self.calc_lab_points() / 10
        expend['provisions'] = 5 * (self.calc_covenfolk_points() / 10))
        expend['armory'] = self.armory / 320
        expend['tithes'] = sum(self.tithes.values())
        expend['wages'] = 2 * (self.calc_covenfolk_points() / 10)
        expend['writing'] = self.writers + self.covenfolk_tiers['magi']

        savings = self.calc_savings(expend)
        ##TODO: factor in savings

        expenses = sum(expend.values())

        if self.inflation_enabled:
            inflation = calculate_inflation(expenses)
            expenses += inflation
            self.inflation = inflation

        self.expenses = expenses

    def calculate_inflation(self, expenses):
        # Page 65 of Covenant book, inflation should not increase if the year's
        # expenditures decreased that year, and I (@mesona) made the decision
        # that the previous year's inflation should not be factored into this
        # calculation
        inflation = self.inflation
        if expenses >= self.expenses - self.inflation:
            inflation = expenses // 100

        return inflation

    # I need to figure out how to do this
    # list comprehension on cost_savings?
    def calc_savings(self, category):
        app_craft = [crafter for crafter in self.cost_savings if crafter[0] == category]
        return app_craft
    
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
