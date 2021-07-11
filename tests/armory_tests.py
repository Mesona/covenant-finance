#!/usr/bin/env python3

import pytest
from armory import Armory, valid_equipment_type, valid_quality, qualities, types

class DescribeValidQuality:

    @staticmethod
    def it_returns_true_on_expected_qualities():
        for quality in qualities:
            assert valid_quality(quality)

    @staticmethod
    def it_returns_false_on_unexpected_qualities():
        assert valid_quality("") == False
        assert valid_quality("TACOS!") == False
        assert valid_quality("YO OY weapon") == False

    @staticmethod
    def it_is_not_case_sensitive():
        for quality in qualities:
            assert valid_quality(quality.upper())
        
        assert valid_quality("StAnDaRd")


class DescribeValidEquipmentType:
    types = ["weapon", "partial", "full", "light siege", "heavy siege"]

    @staticmethod
    def it_returns_true_on_expected_types():
        for t in types:
            assert valid_equipment_type(t)

    @staticmethod
    def it_returns_false_on_unexpected_types():
        assert valid_equipment_type("TUESDAYS!") == False
        assert valid_equipment_type("weapon partial") == False

    @staticmethod
    def it_is_not_case_sensitive():
        for t in types:
            assert valid_equipment_type(t.upper())

        assert valid_equipment_type("WeApOn") == True


class DescribeArmory:
    @staticmethod
    def it_initializes_correctly():
        from collections import defaultdict
        armory = Armory()
        assert isinstance(armory.weapons, defaultdict)
        assert isinstance(armory.full, defaultdict)
        assert isinstance(armory.partial, defaultdict)
        assert isinstance(armory.light_siege, defaultdict)
        assert isinstance(armory.heavy_siege, defaultdict)

    @staticmethod
    def it_selects_the_proper_equipment_types():
        from collections import defaultdict
        armory = Armory()
        weapon = armory.select_equipment_type("weapon")
        full = armory.select_equipment_type("full")
        partial = armory.select_equipment_type("partial")
        heavy_siege = armory.select_equipment_type("heavy_siege")
        light_siege = armory.select_equipment_type("light_siege")

        assert isinstance(weapon, defaultdict)
        assert isinstance(full, defaultdict)
        assert isinstance(partial, defaultdict)
        assert isinstance(heavy_siege, defaultdict)
        assert isinstance(light_siege, defaultdict)

    @staticmethod
    def it_adds_equipment():
        armory = Armory()
        armory.add_equipment("sword", "weapon", "inexpensive")
        assert armory.weapons["sword"]["inexpensive"] == 1
        armory.add_equipment("sword", "weapon", "inexpensive")
        assert armory.weapons["sword"]["inexpensive"] == 2
        armory.add_equipment("half plate", "partial", "standard")
        armory.add_equipment("battering ram", "light siege", "expensive")
        armory.add_equipment("trebuchet", "heavy siege", "expensive")
        assert armory.partial["half plate"]["standard"] == 1
        assert armory.light_siege["battering ram"]["expensive"] == 1
        assert armory.heavy_siege["trebuchet"]["expensive"] == 1

    @staticmethod
    def it_removes_equipment():
        armory = Armory()
        armory.add_equipment("sword", "weapon", "inexpensive")
        armory.add_equipment("sword", "weapon", "inexpensive")
        armory.add_equipment("half plate", "partial", "standard")
        armory.add_equipment("battering ram", "light siege", "expensive")
        armory.add_equipment("trebuchet", "heavy siege", "expensive")

        armory.remove_equipment("sword", "weapon", "inexpensive")
        assert armory.weapons["sword"]["inexpensive"] == 1
        armory.remove_equipment("sword", "weapon", "inexpensive")
        assert armory.weapons["sword"]["inexpensive"] == 0
        armory.remove_equipment("half plate", "partial", "standard")
        armory.remove_equipment("battering ram", "light siege", "expensive")
        armory.remove_equipment("trebuchet", "heavy siege", "expensive")
        assert armory.partial["half plate"]["standard"] == 0
        assert armory.light_siege["battering ram"]["expensive"] == 0
        assert armory.heavy_siege["trebuchet"]["expensive"] == 0

    @staticmethod
    def it_calculates_type_points():
        armory = Armory()
        armory.add_equipment("sword", "weapon", "inexpensive")
        assert armory.calculate_upkeep_points_of("weapon") == 1
        armory.add_equipment("sword", "weapon", "inexpensive")
        assert armory.calculate_upkeep_points_of("weapon") == 2
        armory.add_equipment("rapier", "weapon", "standard")
        assert armory.calculate_upkeep_points_of("weapon") == 6
        armory.add_equipment("greatsword", "weapon", "expensive")
        assert armory.calculate_upkeep_points_of("weapon") == 22

        armory.add_equipment("half plate", "partial", "standard")
        assert armory.calculate_upkeep_points_of("partial") == 8
        armory.add_equipment("half plate", "partial", "inexpensive")
        assert armory.calculate_upkeep_points_of("partial") == 10
        armory.add_equipment("half plate", "partial", "expensive")
        assert armory.calculate_upkeep_points_of("partial") == 42

        armory.add_equipment("full plate", "full", "expensive")
        assert armory.calculate_upkeep_points_of("full") == 64
        armory.add_equipment("full chain", "full", "expensive")
        armory.add_equipment("full monty", "full", "expensive")
        armory.add_equipment("full circus", "full", "expensive")
        assert armory.calculate_upkeep_points_of("full") == 256
        armory.add_equipment("full cloth", "full", "inexpensive")
        assert armory.calculate_upkeep_points_of("full") == 260
        armory.add_equipment("full cloth", "full", "standard")
        assert armory.calculate_upkeep_points_of("full") == 276

        armory.add_equipment("battering ram", "light siege", "expensive")
        assert armory.calculate_upkeep_points_of("light siege") == 16

        armory.add_equipment("trebuchet", "heavy siege", "expensive")
        assert armory.calculate_upkeep_points_of("heavy siege") == 32

    @staticmethod
    def it_calculates_total_points():
        armory = Armory()
        armory.add_equipment("sword", "weapon", "inexpensive")
        armory.add_equipment("sword", "weapon", "inexpensive")
        armory.add_equipment("rapier", "weapon", "standard")
        armory.add_equipment("greatsword", "weapon", "expensive")

        armory.add_equipment("half plate", "partial", "standard")
        armory.add_equipment("half plate", "partial", "inexpensive")
        armory.add_equipment("half plate", "partial", "expensive")

        armory.add_equipment("full plate", "full", "expensive")
        armory.add_equipment("full chain", "full", "expensive")
        armory.add_equipment("full monty", "full", "expensive")
        armory.add_equipment("full circus", "full", "expensive")
        armory.add_equipment("full cloth", "full", "inexpensive")
        armory.add_equipment("full cloth", "full", "standard")

        armory.add_equipment("battering ram", "light siege", "expensive")

        armory.add_equipment("trebuchet", "heavy siege", "expensive")
        assert armory.calculate_total_upkeep_points() == 388
