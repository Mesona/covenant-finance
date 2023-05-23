#!/usr/bin/env python3


SAVING_CATEGORIES = [
        "buildings",
        "consumables",
        "laboratories",
        "provisions",
        "weapons and armor",
        "writing",
        "other",
]

COVENFOLK_CLASSIFICATIONS = [
        "magi",
        "noble",
        "companion",
        "crafter",
        "specialist",
        "dependant",
        "grog",
        "laborer",
        "servant",
        "teamster",
        "horse",
]

def validate_classification(classification):
    if classification not in COVENFOLK_CLASSIFICATIONS:
        raise ValueError(f"""
{classification} is not in the list of classifications!
Please choose between these options: {COVENFOLK_CLASSIFICATIONS}
""")

    return classification

def validate_saving_category(category):
    if category and category not in SAVING_CATEGORIES:
        raise ValueError(f"""
{category} is not in the list of categories!
Please choose between these options: {SAVING_CATEGORIES}
""")

    return category

class Covenfolken:
    def __init__(self):
        self.covenfolk = {}

    def get_covenfolk_classifications(self):
        return COVENFOLK_CLASSIFICATIONS

    def calculate_savings_of(self, saving_category):
        from collections import defaultdict

        matching_folk = [person for person in self.covenfolk.values() if person.saving_category == saving_category]
        potential_savings = defaultdict(int)

        for folk in matching_folk:
            if saving_category == "provisions" and folk.classification == "laborer":
                potential_savings["laborer"] += 1
                continue

            current_profession = folk.profession
            provided_savings = 1 + (folk.skill // (1 if folk.rarity == "rare" else 2))
            potential_savings[current_profession] += provided_savings

        return potential_savings

    def calculate_all_savings(self):
        provided_savings = {}

        for category in SAVING_CATEGORIES: 
            # "other" is a category beause covenants may have specialists that do not contribute to cost savings
            if category != "other":
                provided_savings[category] = self.calculate_savings_of(category)

        return provided_savings

    def total_count_of(self, class_or_profession):
        individuals = [person for person in self.covenfolk.values() if person.classification == class_or_profession]
        if individuals == []:
            individuals = [person for person in self.covenfolk.values() if person.profession == class_or_profession]

        return len(individuals)

    def add_covenfolk(self, *args):
        # Allows the passing of either a Covenfolk object or the parameters
        # to create a Covenfolk
        if isinstance(args[0], Covenfolk):
            folk = args[0]
            if self.is_name_unique(folk.name):
                self.covenfolk[folk.name] = folk
            else:
                raise ValueError(f"Covenfolk name {folk.name} is not unique!")
        else:
            if self.is_name_unique(args[0]):
                folk = Covenfolk(*args)
                self.covenfolk[folk.name] = folk

    def is_name_unique(self, name):
        if name not in self.covenfolk.keys():
            return True

        return False

    def remove_covenfolk(self, name):
        self.covenfolk.pop(name)

    def display_covenfolk(self, name=None):
        if name:
            covenfolk = self.covenfolk[name]
            print(f"{covenfolk.name} {covenfolk.classification}")
            if covenfolk.saving_category:
                print(f"""Savings Category: {covenfolk.saving_category}
{covenfolk.profession}: {covenfolk.skill}
Rarity: {covenfolk.rarity}""")
            print("")

        else:
            for covenfolk in self.covenfolk.values():
                print(f"{covenfolk.name}: {covenfolk.classification}")
                if covenfolk.saving_category:
                    print(f"""Savings Category: {covenfolk.saving_category}
{covenfolk.profession}: {covenfolk.skill}""")
                print("")

    def list(self):

        print(list(self.covenfolk.keys()))

    def get_covenfolk_of_classification(self, classification):
        matches = [covenfolk for _, covenfolk in self.covenfolk.items() if covenfolk.classification == classification]
        return matches


class Covenfolk:
    def __init__(self, name, classification, profession="", saving_category="", skill=0, rarity=""):
        self.name = name
        self.classification = validate_classification(classification)
        self.saving_category = validate_saving_category(saving_category.lower())

        if classification == "laborer":
            self.saving_category = "provisions"

        if classification == "crafter":
            if saving_category == "" or profession == "" or rarity == "":
                raise ValueError("Crafters need a profession and a saving category!")

        self.profession = profession.lower()
        self.set_skill(skill)
        self.rarity = rarity

    def change_profession(self, profession):
        self.profession = profession

    def set_skill(self, value):
        if value < 0:
            raise ValueError("Skills cannot be below 0!")

        self.skill = value

    def increase_skill(self, value=1):
        self.skill += value

    def reduce_skill(self, value=1):
        new_value = self.skill - value
        if new_value < 0:
            raise ValueError("Cannot lower skills below 0!")

        self.skill = new_value

    def change_name(self, name):
        self.name = name

    def set_saving_category(self, category):
        if validate_saving_category(category):
            self.saving_category = category
