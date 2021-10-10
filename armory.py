#!/usr/bin/env python3

qualities = ["inexpensive", "standard", "expensive"]
types = ["weapon", "partial", "full", "light siege", "heavy siege"]


def valid_quality(quality):
    if quality.lower() in qualities:
        return True

    return False

def valid_equipment_type(equipment_type):
    if equipment_type.lower() in types:
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
}


class Armory:
    def __init__(self):
        from collections import defaultdict
        self.weapons = defaultdict(lambda: defaultdict(int))
        self.full = defaultdict(lambda: defaultdict(int))
        self.partial = defaultdict(lambda: defaultdict(int))
        self.light_siege = defaultdict(lambda: defaultdict(int))
        self.heavy_siege = defaultdict(lambda: defaultdict(int))
        self.magic = defaultdict(lambda: defaultdict(int))

    def select_equipment_type(self, equipment_type):
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

    def add_equipment(self, name, equipment_type, quality):
        if not valid_quality(quality):
            raise ValueError(f"Quality of {quality} is not recognized!")

        if not valid_equipment_type(equipment_type):
            raise ValueError(f"Equipment type {equipment_type} not recognized!")

        et = self.select_equipment_type(equipment_type)
        et[name][quality] += 1

    def remove_equipment(self, name, equipment_type, quality):
        if not valid_quality(quality):
            raise ValueError(f"Quality of {quality} is not recognized!")

        if not valid_equipment_type(equipment_type):
            raise ValueError(f"Equipment type {equipment_type} not recognized!")

        et = self.select_equipment_type(equipment_type)
        if et[name][quality] >= 1:
            et[name][quality] -= 1
        else:
            raise ValueError("Cannot have negative quantities!")

    def calculate_upkeep_points_of(self, equipment_type):
        points = 0

        et = self.select_equipment_type(equipment_type)
        for equipment in et.keys():
            for quality in qualities:
                this_amount = et[equipment][quality]
                this_cost = cost_conversion[equipment_type][quality]
                points += this_amount * this_cost

        return points

    def calculate_total_upkeep_points(self):
        total_points = 0
        for equipment_type in types:
            total_points += self.calculate_upkeep_points_of(equipment_type)

        return total_points
