#!/usr/bin/env python3

from collections import defaultdict

EQUIPMENT_QUALITIES = ["inexpensive", "standard", "expensive", "magic"]
EQUIPMENT_TYPES = ["weapon", "partial", "full", "light siege", "heavy siege", "magic"]

SAVINGS_CATEGORIES = [
        "buildings",
        "consumables",
        "laboratories",
        "provisions",
        "weapons and armor",
        "writing",
        "servants",
]

def valid_quality(quality):
    if quality.lower() in EQUIPMENT_QUALITIES:
        return True

    return False

def valid_equipment_type(equipment_type):
    if equipment_type.lower() in EQUIPMENT_TYPES:
        return True

    return False


cost_conversion = {
        "weapon": {
                "inexpensive": 1,
                "standard": 4,
                "expensive": 16
        },
        "partial": {
                "inexpensive": 2,
                "standard": 8,
                "expensive":32 
        },
        "full": {
                "inexpensive": 4,
                "standard": 16,
                "expensive":64
        },
        "light siege": {
                "inexpensive": 0,
                "standard": 0,
                "expensive": 16
        },
        "heavy siege": {
                "inexpensive": 0,
                "standard": 0,
                "expensive": 32
        },
        "magic": {
            "magic": 0,
        }
}


class Armory:
    def __init__(self):
        from collections import defaultdict
        self.weapons = defaultdict(lambda: defaultdict(int))
        self.full = defaultdict(lambda: defaultdict(int))
        self.partial = defaultdict(lambda: defaultdict(int))
        self.light_siege = defaultdict(lambda: defaultdict(int))
        self.heavy_siege = defaultdict(lambda: defaultdict(int))
        self.magic = []

    def calculate_all_savings(self) -> dict:
        """Generates a dictionary of all the covenant savings this armory provides."""
        provided_savings = defaultdict()

        for category in SAVINGS_CATEGORIES:
            provided_savings[category] = {}
            provided_savings[category]["magic"] = self.calculate_savings_of(category)

        return provided_savings

    def calculate_savings_of(self, saving_category: str) -> int:
        """Finds magic items of corresponding saving_category and sums their savings."""
        matching_items = [item for item in self.magic if item["saving_category"] == saving_category]
        potential_savings = 0

        for item in matching_items:
            potential_savings += item["saving_value"]

        return potential_savings

    def select_equipment_type(self, equipment_type: str):
        """Returns all of the selected equipment type."""
        equipment_type = equipment_type.replace(" ", "_")
        if equipment_type == "weapon":
            return self.weapons
        elif equipment_type == "partial":
            return self.partial
        elif equipment_type == "full":
            return self.full
        elif equipment_type == "light_siege":
            return self.light_siege
        elif equipment_type == "heavy_siege":
            return self.heavy_siege
        elif equipment_type == "magic":
            return self.magic
        else:
            raise ValueError(f"Invalid equipment type of {equipment_type}!")

    def add_equipment(
            self,
            name: str,
            equipment_type: str,
            quality: str,
            saving_category="",
            saving_value=0,
            description=""
        ) -> None:
        """Adds a single piece of equipment to an Armory instance."""
        if not valid_quality(quality):
            raise ValueError(f"Quality of {quality} is not recognized!")

        if not valid_equipment_type(equipment_type):
            raise ValueError(f"Equipment type {equipment_type} not recognized!")

        if saving_category and equipment_type != "magic":
            raise ValueError(f"Only 'magic' items can provide savings, not {equipment_type}!")

        if equipment_type == "magic" and saving_category.lower() not in SAVINGS_CATEGORIES:
            raise ValueError(f"{saving_category} is not one of the listed saivng categories!")

        et = self.select_equipment_type(equipment_type)
        if equipment_type == "magic":
            self.magic.append(
                    {
                        "name": name,
                        "saving_category": saving_category,
                        "saving_value": saving_value,
                        "description": description,
                    }
            )
        else:
            et[name][quality] += 1

        return "Successfully added equipment!"

    def remove_equipment(
            self,
            name: str,
            equipment_type: str,
            quality: str
        ) -> str:
        """Removes a single piece of equipment from an Armory instance."""
        if not valid_quality(quality):
            raise ValueError(f"Quality of {quality} is not recognized!")

        if not valid_equipment_type(equipment_type):
            raise ValueError(f"Equipment type {equipment_type} not recognized!")

        et = self.select_equipment_type(equipment_type)
        if et[name][quality] >= 1:
            et[name][quality] -= 1
        else:
            raise ValueError("Cannot have negative quantities!")

        return "Successfully removed equipment!"

    def calculate_upkeep_points_of(self, equipment_type: str) -> int:
        """
        Returns the total upkeep cost of all equipment that falls under a
        specified equipment type.
        """

        points = 0

        equipment_qualities = EQUIPMENT_QUALITIES.copy()
        equipment_qualities.remove("magic")

        et = self.select_equipment_type(equipment_type)
        for equipment in et.keys():
            for quality in equipment_qualities:
                this_amount = et[equipment][quality]
                this_cost = cost_conversion[equipment_type][quality]
                points += this_amount * this_cost

        return points

    def calculate_total_upkeep_points(self) -> int:
        """
        Returns the total upkeep point value of all items within a single
        Armroy instance.
        """
        equipment_types = EQUIPMENT_TYPES.copy()
        equipment_types.remove("magic")

        total_points = 0
        for equipment_type in equipment_types:
            total_points += self.calculate_upkeep_points_of(equipment_type)

        return total_points
