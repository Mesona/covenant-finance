def validate_classification(classification):
    classifications = [
            "mage",
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

    if classification not in classifications:
        raise ValueError(f"""
{classification} is not in the list of classifications!
Please choose between these options: {classifications}
""")

    return classification

def validate_saving_category(category):
    categories = [
            "buildings",
            "consumables",
            "laboratories",
            "provisions",
            "weapons and armor",
            "writing materials",
    ]

    if category and category not in categories:
        raise ValueError(f"""
{category} is not in the list of categories!
Please choose between these options: {categories}
""")

    return category

class Covenfolken:
    def __init__(self):
        self.covenfolk = {}

    def calculate_savings(self, saving_category):
        saving_potential = [person.skill for person in self.covenfolk if person.saving_category == saving_category]
        return saving_potential

    def total(self, class_or_profession):
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

    def display(self):
        for covenfolk in self.covenfolk.values():
            print(f"{covenfolk.name}: {covenfolk.classification}")
            if covenfolk.saving_category:
                print(f"""Savings Category: {covenfolk.saving_category}
{covenfolk.profession}: {covenfolk.skill}""")
            print("")

    def list(self):

        print(list(self.covenfolk.keys()))


class Covenfolk:
    def __init__(self, name, classification, profession="", saving_category="", skill=0):
        self.name = name
        self.classification = validate_classification(classification)
        self.profession = profession.lower()
        self.saving_category = validate_saving_category(saving_category.lower())
        self.set_skill(skill)

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
