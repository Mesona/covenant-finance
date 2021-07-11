#!/usr/bin/env python3

class Laboratories:
    def __init__(self):
        from collections import defaultdict
        self.labs = defaultdict(bool)

    def is_lab_name_unique(self, name):
        if self.labs[name]:
            return False

        return True

    def add_lab(self, *args):
        if isinstance(args[0], Laboratory):
            lab = Laboratory.name
            if self.is_lab_name_unique(lab.name):
                self.labs[lab.name] = lab
            else:
                raise ValueError(f"Lab name {lab.name} is not unique!")
        else:
            if self.is_lab_name_unique(args[0]):
                lab = Laboratory(*args)
                self.labs[lab.name] = lab

    def remove_lab(self, name):
        self.labs.pop(name)

    def calculate_total_point_costs(self):
        total_points = 0
        for lab in self.labs.keys():
            total_points += lab.calculate_annual_points()

        def return_total_points


class Laboratory:
    def __init__(
            self,
            name,
            owner="",
            size=0,
            virtue_points=0,
            flaw_points=0,
            extra_upkeep=0,
            usage="typical",
            minor_fortifications=0,
            major_fortifications=0,
    ):
        self.name = name
        self.owner = owner
        self.size = size
        self.vp = virtue_points
        self.fp = flaw_points
        self.extra_upkeep = extra_upkeep
        self.usage = usage
        self.points = self.calculate_annual_points()
        self.minor_fortifications = minor_fortifications
        self.major_fortifications = major_fortifications

    def change_name(self, string):
        self.name = string

    def add_minor_fortification(self, value=1):
        self.minor_fortifications += value

    def remove_minor_fortification(self, value=1):
        new_total = self.minor_fortifications - value
        if new_total < 0:
            raise ValueError("Labs cannot have negative fortifications!")

        self.minor_fortifications = new_total

    def add_major_fortification(self, value=1):
        self.major_fortifications += value

    def remove_major_fortification(self, value=1):
        new_total = self.major_fortifications - value
        if new_total < 0:
            raise ValueError("Labs cannot have negative fortifications!")

        self.major_fortifications = new_total

    def set_size(self, size):
        if size < -5:
            raise ValueError("Laboratories cannot be smaller than size -5")

        self.size = size 
        self.points = self.calculate_annual_points()

    def increase_size(self, size=1):
        self.size += size
        self.points = self.calculate_annual_points()

    def decrease_size(self, size=1):
        new_size = self.size - size
        if new_size <= -5:
            raise ValueError("Laboratories cannot be smaller than size -5")

        self.size = new_size
        self.points = self.calculate_annual_points()

    def change_owner(self, person):
        self.owner = person

    def add_virtue_points(self, vp=1):
        self.vp += vp

    def add_flaw_points(self, fp=1):
        self.fp += fp

    def remove_virtue_points(self, vp=1):
        self.vp -= vp

    def remove_flaw_points(self, fp=1):
        self.fp -= fp

    def set_extra_upkeep(self, upkeep):
        self.extra_upkeep = upkeep
        self.points = self.calculate_annual_points()

    def add_extra_upkeep(self, upkeep=1):
        self.extra_upkeep += upkeep
        self.points = self.calculate_annual_points()

    def remove_extra_upkeep(self, upkeep=1):
        self.extra_upkeep -= upkeep
        self.points = self.calculate_annual_points()

    def change_usage(self, usage):
        if not usage.lower() in ["light", "typical", "heavy"]:
            raise ValueError("Usage can only be 'light', 'typical', or 'heavy'")

        self.usage = usage.lower()
        self.points = self.calculate_annual_points()

    def calculate_annual_points(self):
        upkeep_points_multiplier = 0
        if self.usage == "light":
            upkeep_points_multiplier = 0.5
        elif self.usage == "typical":
            upkeep_points_multiplier = 1
        elif self.usage == "heavy":
            upkeep_points_multiplier = 1.5

        # TODO: Figure out the equation to make this dynamic
        base_lab_points = {
               -5: 1,
               -4: 2,
               -3: 3,
               -2: 5,
               -1: 7,
               0: 10,
               1: 15,
               2: 30,
               3: 60,
               4: 100,
               5: 150
        }

        total_points = base_lab_points[self.size + self.extra_upkeep] * upkeep_points_multiplier
        return total_points
