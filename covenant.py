#!/usr/bin/env python3

import math
from covenfolk import Covenfolken
from armory import Armory
from laboratory import Laboratories
from collections import defaultdict
from models import CovenantModel

base_covenfolk_point_costs = {
        "magi": 5,
        "noble": 5,
        "companion": 3,
        "crafter": 2,
        "specialist": 2,
        "dependant": 1,
        "grog": 2,
        "laborer": 2,
        "servant": 2,
        "teamster": 2,
        "covenfolk": 1,
        "horse": 1,
}


def save_covenant(covenant, path):
    import jsonpickle
    if covenant.expenses == float("inf"):
        covenant.expenses = 9999999
    dump = jsonpickle.encode(covenant, indent=4)
    with open(path, "w+") as f:
        f.write(dump)

    print(f"Covenant successfully saved to {path}")
        

def load_covenant(path):
    import jsonpickle
    cov = CovenantModel.query.filter(CovenantModel.
    with open(path, "r") as f:
        covenant = jsonpickle.loads(f.read())
    print(f"Covenant successfully loaded from {path}")
    return covenant


class Covenant:
    def __init__(
            self,
            name = "Vernus",
            season = "spring",
            income_sources = {"source": 100},
            tithes = {},
            treasury = 50.0,
            laboratories = {},
            inflation_enabled = True,
            inflation = 0,
        ):
        self.name = name

        if season.lower() in ["spring", "summer", "winter", "autumn"]:
            self.season = season.lower()
        else:
            raise ValueError(f"""
Season {season} is not an accepted covenant season!
Please select between spring, summer, autumn, and winter.
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
        self.laboratories = Laboratories()
        self.armory = Armory()
        self.treasury = treasury
        self.inflation_enabled = inflation_enabled
        self.inflation = inflation
        self.expenses = float("inf")  # Prevents inflation from taking effect the first year
            
    def calc_covenfolk_points(self):
        point_cost = 0
        for covenfolk in self.covenfolken.covenfolk.values():
            point_cost += self.calculate_covenfolk_point_costs(covenfolk.classification) 
        return point_cost

    def calculate_covenfolk_point_costs(self, classification):
        if self.season in ["spring", "winter"] or classification == "horse":
            return base_covenfolk_point_costs[classification]
        else:
            return base_covenfolk_point_costs[classification] * 2

    def calc_servant_minimum(self):
        covenfolk_roles = ["magi", "noble", "companion", "crafter", "specialist", "dependant", "grog", "horse"]
        covenfolk_points = 0

        for classification in covenfolk_roles:
            number_of_matching_covenfolk = self.covenfolken.total(classification)
            covenfolk_points += self.calculate_covenfolk_point_costs(classification) * number_of_matching_covenfolk

        servant_minimums = math.ceil(covenfolk_points / 10) * 2
        return servant_minimums

    def calc_teamster_minimum(self):
        covenfolk_roles = ["magi", "noble", "companion", "crafter", "specialist", "dependant", "grog", "horse", "servant"]
        covenfolk_points = 0

        for classification in covenfolk_roles:
            number_of_matching_covenfolk = self.covenfolken.total(classification)
            covenfolk_points += self.calculate_covenfolk_point_costs(classification) * number_of_matching_covenfolk

        covenfolk_points -= (self.covenfolken.total('laborer') * 2)
        teamster_minimums = math.ceil(covenfolk_points / 10)
        return teamster_minimums

    def meets_servant_minimum(self):
        servants = self.covenfolken.total("servant")
        return servants >= self.calc_servant_minimum()

    def meets_teamster_minimum(self):
        teamsters = self.covenfolken.total("teamster")
        return teamsters >= self.calc_teamster_minimum()

    def update_expenditures(self):
        previous_expenses = self.expenses
        self.expenses = self.calc_expenditures()
        self.inflation = self.calculate_inflation(previous_expenses, self.expenses)

    def calc_expenditures(self):
        expend = {}
        expend["buildings"] = round(self.calc_covenfolk_points() / 10, 2)
        expend["consumables"] = round(2 * (self.calc_covenfolk_points() / 10), 2)
        expend["laboratories"] = round(self.calc_lab_points() / 10, 2)
        expend["provisions"] = round(5 * (self.calc_covenfolk_points() / 10))
        expend["weapons and armor"] = round(self.armory.calculate_total_upkeep_points() / 320, 2)
        expend["tithes"] = sum(self.tithes.values())
        expend["wages"] = round(2 * (self.calc_covenfolk_points() / 10), 2)
        expend["writing"] = self.covenfolken.total("writer") + self.covenfolken.total("magi")

        savings = self.covenfolken.calculate_all_savings()
        cost_saving_expenses = self.expenditures_and_savings(expend, savings)

        return round(sum(cost_saving_expenses.values()), 2)

    def calculate_inflation(self, previous_expenses, current_expenses):
        # Page 65 of Covenant book, inflation should only increase if the year's
        # expenditures were greater than the previous year's
        inflation = self.inflation
        if current_expenses - previous_expenses > 0:
            inflation = current_expenses // 100

        return inflation

    def expenditures_and_savings(self, expenses, savings):
        # TODO: Expand to factor in magic / magic item savings
        categories = list(savings.keys())
        maximum_cost_savings = {
            "buildings" : 0.5,
            "consumables" : 0.2,
            "laboratories" : 0.2,
            "provisions" : 0.2,
            "weapons and armor" : 0.5,
            "writing" : 0.5,
        }

        # TODO: Break this into own method or function
        for category in categories:
            this_expense = expenses[category]
            this_saving = savings[category]
            max_saving = this_expense * maximum_cost_savings[category]
            for profession in this_saving.keys():
                this_expense -= min(max_saving, this_saving[profession])

            expenses[category] = this_expense

        return expenses


    def calc_lab_points(self):
        points = 0
        for lab in self.laboratories.labs.values():
            points += lab.points
        return points
    
    def total_expenditure(self):
        return self.expenses + self.inflation
                   
    def total_income(self):
        return sum(self.income_sources.values())

    def change_season(self, season):
        self.season = season

    def display_finances(self):
        # TODO: this is broken
        for key, val in self.calc_expenditures().items():
            print(key.ljust(15) + str(val).rjust(8))
        print ('Total:'.ljust(15) + str(self.total_expenditure()).rjust(8))
        print('\nTotal income:' + str(self.total_income()).rjust(10))
        print('Treasury:' + str(self.treasury).rjust(14))
        #print()

    def display_labs(self):
        # TODO: this is broken
        print('Name:'.ljust(15) + 'Upkeep'.rjust(8))
        for key, val in self.laboratories.items():
            print(key.ljust(20) + str(val).rjust(3))
        #print()
    
    def bank(self, silver):
        self.treasury += silver

    def advance_year(self):
        self.update_expenditures()
        self.treasury = self.treasury + self.total_income() - self.total_expenditure()
