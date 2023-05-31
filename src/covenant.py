#!/usr/bin/env python3

import math
from collections import defaultdict
from src.covenfolk import Covenfolken
from src.armory import Armory
from src.laboratory import Laboratories

base_covenfolk_point_costs = {
        "cheap": {
            "magi": 5,
            "noble": 5,
            "companion": 3,
            "crafter": 2,
            "specialist": 2,
            "dependant": 1,
            "grog": 1,
            "laborer": 1,
            "servant": 1,
            "teamster": 1,
            "covenfolk": 1,
            "horse": 1,
        },
        "expensive": {
            "magi": 10,
            "noble": 10,
            "companion": 5,
            "crafter": 3,
            "specialist": 3,
            "dependant": 2,
            "grog": 2,
            "laborer": 2,
            "servant": 2,
            "teamster": 2,
            "covenfolk": 2,
            "horse": 1,
        }
}


def save_covenant(covenant, path=None):
    import jsonpickle
    if covenant.expenses == float("inf"):
        covenant.expenses = 9999999
    frozen = jsonpickle.encode(covenant, keys=True)

    if path:
        with open(path, "w+") as f:
            f.write(frozen)

        print(f"Covenant successfully saved to {path}")
    else:
        return frozen


def load_covenant_from_string(covenant):
    import jsonpickle
    covenant_string = jsonpickle.decode(covenant, keys=True)
    return covenant_string


def load_covenant_from_file(path):
    import jsonpickle

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
            laboratories = Laboratories(),
            covenfolken = Covenfolken(),
            armory = Armory(),
            inflation_enabled = True,
            inflation = 0,
            current_year = 1220,
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
        self.covenfolken = covenfolken
        self.laboratories = laboratories
        self.armory = armory
        self.treasury = treasury
        self.inflation_enabled = inflation_enabled
        self.inflation = inflation
        self.expenses = float("inf")  # Prevents inflation from taking effect the first year
        self.current_year = int(current_year)

    def delete_covenant(self) -> bool:
        for lab in self.laboratories.labs:
            del lab

        self.laboratories.labs = defaultdict(bool)

        for covenfolk in self.covenfolken.covenfolk:
            del covenfolk

        self.covenfolken.covenfolk = {}

        return True

    def calculate_minimum_covenfolk_base_costs(self) -> int:
        covenfolk_roles = ["magi", "noble", "companion", "crafter", "specialist", "dependant", "grog", "horse"]
        covenfolk_points = 0

        for classification in covenfolk_roles:
            number_of_matching_covenfolk = self.covenfolken.total_count_of(classification)
            covenfolk_points += self.calculate_covenfolk_point_costs(classification) * number_of_matching_covenfolk

        return covenfolk_points

    def calculate_covenfolk_points(self):
        point_cost = 0
        for covenfolk in self.covenfolken.covenfolk.values():
            point_cost += self.calculate_covenfolk_point_costs(covenfolk.classification) 
        return point_cost

    def calculate_covenfolk_point_costs(self, classification):
        if self.season in ["spring", "winter"] or classification == "horse":
            return base_covenfolk_point_costs["cheap"][classification]
        else:
            return base_covenfolk_point_costs["expensive"][classification]

    def calculate_servant_minimum(self):
        covenfolk_points = self.calculate_minimum_covenfolk_base_costs()
        print("Covenfolk_points:", covenfolk_points)
        servant_savings = self.armory.calculate_savings_of("servants")
        print("SS:", servant_savings)

        servant_minimums = math.ceil(covenfolk_points / 10) * 2
        laborer_savings = self.armory.calculate_savings_of("servants")
        servant_minimums = servant_minimums - laborer_savings
        return servant_minimums

    def calculate_teamster_minimum(self):
        covenfolk_points = self.calculate_minimum_covenfolk_base_costs()
        covenfolk_points += self.calculate_covenfolk_point_costs("servant") * self.covenfolken.total_count_of("servant")

        covenfolk_points -= (self.covenfolken.total_count_of("laborer") * 2)
        teamster_minimums = math.ceil(covenfolk_points / 10)
        return teamster_minimums

    def meets_laborer_minimum(self):
        laborers = self.covenfolken.total_count_of("laborer")
        return laborers >= self.calculate_servant_minimum()

    def meets_teamster_minimum(self):
        teamsters = self.covenfolken.total_count_of("teamster")
        return teamsters >= self.calculate_teamster_minimum()

    def update_expenditures(self):
        previous_expenses = self.expenses
        self.expenses = self.calculate_expenditures()
        self.inflation = self.calculate_inflation(previous_expenses, self.expenses)

    def calculate_expenditures(self):
        expend = {}
        expend["buildings"] = round(self.calculate_covenfolk_points() / 10, 2)
        expend["consumables"] = round(2 * (self.calculate_covenfolk_points() / 10), 2)
        expend["laboratories"] = round(self.calculate_lab_points() / 10, 2)
        expend["provisions"] = round(5 * (self.calculate_covenfolk_points() / 10))
        expend["weapons and armor"] = round(self.armory.calculate_total_upkeep_points() / 320, 2)
        expend["tithes"] = sum(self.tithes.values())
        expend["wages"] = round(2 * (self.calculate_covenfolk_points() / 10), 2)
        expend["writing"] = self.covenfolken.total_count_of("writer") + self.covenfolken.total_count_of("magi")

        covenfolken_savings = self.covenfolken.calculate_all_savings()
        armory_savings = self.armory.calculate_all_savings()

        savings = defaultdict(lambda: defaultdict())
        def merge(d, new_d):
            for k, v in new_d.items():
                if isinstance(v, dict):
                    merge(d[k], v)
                else:
                    d[k] = d.setdefault(k, 0) + v

        merge(savings, armory_savings)
        merge(savings, covenfolken_savings)

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
            if category == "servants":
                continue

            this_expense = expenses[category]
            this_saving = savings[category]
            max_saving = this_expense * maximum_cost_savings[category]
            for profession in this_saving.keys():
                this_expense -= min(max_saving, this_saving[profession])

            expenses[category] = this_expense

        return expenses


    def calculate_lab_points(self):
        points = 0
        for lab in self.laboratories.labs.values():
            points += lab.points
        return points
    
    def total_expenditure(self):
        return self.expenses + self.inflation
                   
    def total_income(self):
        print("SYM:", self.income_sources.values())
        print("SUM:", sum(self.income_sources.values()))
        return sum(self.income_sources.values())

    def change_season(self, season):
        self.season = season

    def display_finances(self):
        # TODO: this is broken
        for key, val in self.calculate_expenditures().items():
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

    def advance_year(self, additional_costs=0):
        self.update_expenditures()
        self.treasury = round((self.treasury + self.total_income() - self.total_expenditure() - additional_costs), 2)
        self.current_year += 1
        self.armory.advance_charged_items()

