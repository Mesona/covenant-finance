def validate_profession(profession):
    professions = [
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

    if profession not in professions:
        raise InputError(f"{profession} is not in the list of professions!
Please choose between these options: {professions}")

    return profession

def validate_saving_category(category):
    categories = [
            "buildings",
            "consumables",
            "laboratories",
            "provisions",
            "weapons and armor",
            "writing materials",
    ]

    if category not in categories:
        raise InputError(f"{category} is not in the list of categories!
Please choose between these options: {categories}")

    return category

class Covenfolks:
    def __init__():
        self.covenfolk = {}

    def calculate_savings(saving_category):
        saving_potential = [person.skill for person in self.covenfolk if person.saving_category == saving_category]
        return saving_potential

    def total_of(profession):
        individuals = [person for person in self.covenfolk if person.profession == profession]
        return len(individuals)

    def add_covenfolk(name, profession, saving_category="", skill=0):
        self.covenfolk[name] = Covenfolk(name, profession, saving_category, skill))

    def remove_covenfolk(name)
        self.covenfolk.pop(name)


class Covenfolk:
    def __init__(name, profession, saving_category="", skill=0):
        self.name = name
        self.profession = validate_profession(profession)
        self.saving_category = validate_saving_category(saving_category.lower())
        self.skill = self.set_skill(skill)


    def set_skill(self, value):
        self.skill = value

    def increase_skill(self, value=1):
        self.skil += value

    def reduce_skill(self, value=1):
        new_value = self.skill - value
        if new_value < 0:
            raise InputError("Cannot lower skills below 0!")

        self.skill = new_value

    def change_name(self, name):
        self.name = name

    def set_saving_category(self, category):
        if validate_saving_category(category):
            self.saving_category = category
