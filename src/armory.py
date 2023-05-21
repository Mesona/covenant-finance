#!/usr/bin/env python3

from collections import defaultdict

EQUIPMENT_QUALITIES = ["inexpensive", "standard", "expensive", "magic", "charged"]
EQUIPMENT_TYPES = ["weapon", "partial", "full", "light siege", "heavy siege", "magic", "charged"]

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
        },
        "charged": {
            "charged": 0,
        }
}


class Armory:
    def __init__(self):
        from collections import defaultdict
        self.weapons = defaultdict(dict)
        self.full = defaultdict(dict)
        self.partial = defaultdict(dict)
        self.light_siege = defaultdict(dict)
        self.heavy_siege = defaultdict(dict)
        self.magic = []
        self.charged = []
        self.equipment = {
                "weapons": self.weapons,
                "partial": self.partial,
                "full": self.full,
                "light_siege": self.light_siege,
                "heavy_siege": self.heavy_siege,
                "magic": self.magic,
                "charged": self.charged,
        }

    def calculate_all_savings(self) -> dict:
        """Generates a dictionary of all the covenant savings this armory provides."""
        provided_savings = {}

        for category in SAVINGS_CATEGORIES:
            provided_savings[category] = {}
            provided_savings[category]["magic"] = self.calculate_savings_of(category)

        return provided_savings

    def calculate_savings_of(self, saving_category: str) -> int:
        """Finds magic items of corresponding saving_category and sums their savings."""
        potential_savings = 0
        matching_magic_items = [item for item in self.magic if item["saving_category"] == saving_category] 
        matching_charged_items = [item for item in self.charged if item["saving_category"] == saving_category] 

        for item in matching_magic_items:
            potential_savings += item["saving_value"]

        for item in matching_charged_items:
            if item.magic_item_years_worth_of_charges != 0:
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
        elif equipment_type == "charged":
            return self.charged
        else:
            raise ValueError(f"Invalid equipment type of {equipment_type}!")

    # TODO: Add test for me
    def list_equipment_type(self, equipment_type: str) -> list:
        """Returns a list of dictionaries, one per item, for use with front end displays."""
        equipment_target = self.select_equipment_type(equipment_type)
        equipment = []
        if equipment_type == "magic":
            return equipment_target
        elif equipment_type == "charged":
            return equipment_target
        else:
            for equip, data in equipment_target.items():
                for quality, quantity in data.items():
                    for _ in range(quantity):
                        equipment.append({
                            "name": equip,
                            "quality": quality
                        })

        return equipment

    def add_equipment(
            self,
            name: str,
            equipment_type: str,
            quality: str,
            saving_category="",
            saving_value=0,
            description="",
            charged_item_currently_active=False,
            magic_item_years_worth_of_charges=0,
        ) -> None:
        """Adds a single piece of equipment to an Armory instance."""
        if not valid_quality(quality):
            raise ValueError(f"Quality of {quality} is not recognized!")

        if not valid_equipment_type(equipment_type):
            raise ValueError(f"Equipment type {equipment_type} not recognized!")

        if saving_category and (equipment_type != "magic" and equipment_type != "charged"):
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
                        "charged_item_currently_active": charged_item_currently_active,
                        "magic_item_years_worth_of_charges": magic_item_years_worth_of_charges,
                    }
            )
        if equipment_type == "charged":
            self.charged.append(
                    {
                        "name": name,
                        "saving_category": saving_category,
                        "saving_value": saving_value,
                        "description": description,
                        "charged_item_currently_active": charged_item_currently_active,
                        "magic_item_years_worth_of_charges": magic_item_years_worth_of_charges,
                    }
            )
        else:
            if not et[name]:
                et[name] = defaultdict(int)

            et[name][quality] += 1

        return "Successfully added equipment!"

    def get_charged_items(self) -> list:
        charged_items = []
        charged_items = self.select_equipment_type("charged")
        for key, val in charged_items.items():
            if val["charged"]:
                charged_items.append(val)

        return charged_items

    def advance_charged_items(self) -> bool:
        charged_items = self.select_equipment_type("charged")

        if not charged_items:
            return True

        for key, val in charged_items.items():
            if val["charged_item_currently_active"] and val["magic_item_years_worth_of_charges"]:
                self.charged[key].magic_item_years_worth_of_charges -= 1

        return True



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
        if not et[name]:
            et[name] = defaultdict(int)

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
        equipment_qualities.remove("charged")

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
        equipment_types.remove("charged")

        total_points = 0
        for equipment_type in equipment_types:
            total_points += self.calculate_upkeep_points_of(equipment_type)

        return total_points
