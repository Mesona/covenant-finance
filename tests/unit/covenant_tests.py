# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring

import pytest
import os

from src.covenfolk import Covenfolk
from src.covenant import Covenant
from src.armory import Armory
from src.sample_covenants import semita

covenfolken = {
    'magi' : 6,
    'noble' : 0,
    'companion' : 4,
    'crafter' : 0,
    'specialist': 3,
    'dependant': 0,
    'grog': 10,
    'laborer' : 12,
    'teamster' : 7,
    'horse': 0
}

@pytest.fixture(autouse=True)
def clean_env():
    """Ensures no environment bleed occurrs, and errors if it somehow fails."""

    os.environ["cleaned"] = "false"
    old_env = os.environ.copy()
    os.environ["cleaned"] = "true"

    try:
        yield
    finally:
        os.environ.clear()
        os.environ.update(old_env)
        assert os.environ["cleaned"] == "false"
        assert os.environ.get("env") is None

@pytest.fixture
def set_and_clean_up_semita():
    """Helps semita based tests run in parllel."""
    s = semita()

    yield s

    s.delete_covenant()

@pytest.fixture
def default_covenant():
    cov = Covenant()

    yield cov

    cov.delete_covenant()


def custom_covenant():
    cov = Covenant(
            name = "Lorem",
            season = "autumn",
            income_sources = {"source": 250, "source2": 100},
            tithes = {"Lord Farqua": 10},
            treasury = 75.5,
            inflation_enabled = False,
            inflation = 10,
    )
    return cov

class DescribeCovenant:
    @staticmethod
    def it_initializes_with_default_values(default_covenant):
        assert default_covenant.name == "Vernus"
        assert default_covenant.season == "spring"
        assert default_covenant.income_sources == {"source": 100}
        assert default_covenant.tithes == {}
        assert default_covenant.treasury == 50.0
        assert default_covenant.covenfolken.covenfolk == {}
        assert default_covenant.laboratories.labs == {}
        assert isinstance(default_covenant.armory, Armory)
        assert default_covenant.inflation_enabled is True
        assert default_covenant.inflation == 0

    @staticmethod
    def it_initializes_with_custom_values():
        cov = custom_covenant()
        assert cov.name == "Lorem"
        assert cov.season == "autumn"
        assert cov.income_sources == {"source": 250, "source2": 100}
        assert cov.tithes == {"Lord Farqua": 10}
        assert cov.treasury == 75.5
        assert cov.covenfolken.covenfolk == {}
        assert cov.inflation_enabled is False
        assert cov.inflation == 10
        cov.delete_covenant()

    # FIXME: These 3 tests somehow cause env bleed
    #@staticmethod
    #def it_can_initialize_semita(set_and_clean_up_semita):
    #    assert set_and_clean_up_semita

    #@staticmethod
    #def it_calculates_semita_servant_requirements_same_as_book(set_and_clean_up_semita):
    #    assert set_and_clean_up_semita.calculate_servant_minimum() == 16

    #@staticmethod
    #def it_calculates_semita_teamster_requirements_same_as_book(set_and_clean_up_semita):
    #    assert set_and_clean_up_semita.calculate_teamster_minimum() == 4

    @staticmethod
    def it_can_change_seasons(default_covenant):
        default_covenant.change_season("autumn")
        assert default_covenant.season == "autumn"

    @staticmethod
    def it_correctly_capitalizes_season(default_covenant):
        default_covenant.change_season("WINTER")
        assert default_covenant.season == "winter"

    @staticmethod
    def it_does_not_accept_custom_seaons():
        with pytest.raises(ValueError):
            Covenant(season = "flamebroiled")

    @staticmethod
    def it_errors_when_bad_income_sources_are_added():
        with pytest.raises(TypeError):
            Covenant(income_sources = {"source": "abc"})

        with pytest.raises(TypeError):
            Covenant(income_sources = {1: 200})

    @staticmethod
    def it_calculates_income_source_changes(default_covenant):
        default_covenant.advance_year()
        assert default_covenant.treasury == 150.0
        default_covenant.income_sources["wishing well"] = 250
        default_covenant.advance_year()
        assert default_covenant.treasury == 500.0

    @staticmethod
    def it_calculates_covenfolk_changes(default_covenant):
        folk = Covenfolk("george", "magi")
        default_covenant.covenfolken.add_covenfolk(folk)
        assert default_covenant.covenfolken.covenfolk["george"] == folk

    @staticmethod
    def it_calculates_season_changes(default_covenant):
        folk = Covenfolk("george", "magi")
        default_covenant.covenfolken.add_covenfolk(folk)
        assert default_covenant.calculate_expenditures() == 5.5
        default_covenant.change_season("autumn")
        assert default_covenant.calculate_expenditures() == 11.0

    @staticmethod
    def it_calculates_treaury_changes(default_covenant):
        default_covenant.bank(10)
        assert default_covenant.treasury == 60.0
        default_covenant.bank(-100)
        assert default_covenant.treasury == -40.0

    @staticmethod
    def it_calculates_lab_cost_saving_changes(default_covenant):
        default_covenant.laboratories.add_lab("route 66")
        default_covenant.laboratories.add_lab("route 67")
        default_covenant.laboratories.add_lab("route 68")
        default_covenant.laboratories.add_lab("route 69")
        assert default_covenant.calculate_expenditures() == 4.0
        default_covenant.covenfolken.add_covenfolk("worker", "crafter", "brickmaker", "laboratories", 2, "common")
        assert default_covenant.calculate_expenditures() == 5.2
        default_covenant.covenfolken.add_covenfolk("worker 2", "crafter", "brickmaker", "laboratories", 10, "rare")
        assert default_covenant.calculate_expenditures() == 7.2

    @staticmethod
    def it_correctly_factors_cost_saving_caps_per_profession(default_covenant):
        default_covenant.laboratories.add_lab("route 66", "aye", 5)
        assert default_covenant.calculate_expenditures() == 15.0
        default_covenant.covenfolken.add_covenfolk("worker", "crafter", "brickmaker", "laboratories", 200, "common")
        assert default_covenant.calculate_expenditures() == 14.0

    @staticmethod
    def it_calculates_laboratory_changes(default_covenant):
        assert default_covenant.calculate_expenditures() == 0.0
        default_covenant.laboratories.add_lab("route 66")
        assert default_covenant.calculate_expenditures() == 1.0

    @staticmethod
    def it_can_verify_too_few_teamsters_exist(default_covenant):
        default_covenant.covenfolken.add_covenfolk("Mary", "magi")
        assert default_covenant.meets_laborer_minimum() == False
        default_covenant.covenfolken.add_covenfolk("Todd", "laborer")
        default_covenant.covenfolken.add_covenfolk("Tammy", "laborer")
        assert default_covenant.meets_laborer_minimum() == True
        
    @staticmethod
    def it_can_verify_too_few_laborers_exist(default_covenant):
        default_covenant.covenfolken.add_covenfolk("Arg", "magi")
        assert default_covenant.meets_teamster_minimum() == False
        default_covenant.covenfolken.add_covenfolk("Teamster", "teamster")
        assert default_covenant.meets_teamster_minimum() == True

    @staticmethod
    def it_correctly_factors_in_laborers_for_teamster_requirements(default_covenant):
        default_covenant.covenfolken.add_covenfolk("Arg", "magi")
        default_covenant.covenfolken.add_covenfolk("gle", "magi")
        default_covenant.covenfolken.add_covenfolk("Barg", "magi")
        assert default_covenant.meets_teamster_minimum() == False
        default_covenant.covenfolken.add_covenfolk("le", "dependant")
        default_covenant.covenfolken.add_covenfolk("woo", "dependant")
        default_covenant.covenfolken.add_covenfolk("tem", "teamster")
        assert default_covenant.meets_teamster_minimum() == False
        default_covenant.covenfolken.add_covenfolk("lab", "laborer")
        default_covenant.covenfolken.add_covenfolk("orer", "laborer")
        assert default_covenant.meets_teamster_minimum() == False

    @staticmethod
    def it_correctly_calculates_inflation(default_covenant):
        default_covenant.inflation = 0
        assert default_covenant.calculate_inflation(100, 200) == 2

    @staticmethod
    def it_does_not_increase_inflation_if_expenses_lowered(default_covenant):
        default_covenant.inflation = 5
        assert default_covenant.calculate_inflation(300, 150) == 5

    @staticmethod
    def it_calculates_armory_increases(default_covenant):
        default_covenant.armory.add_equipment("sword", "weapon", "expensive")
        assert default_covenant.calculate_expenditures() == 0.05
        default_covenant.armory.add_equipment("Missle", "heavy siege", "expensive")
        default_covenant.armory.add_equipment("Missle", "heavy siege", "expensive")
        default_covenant.armory.add_equipment("Missle", "heavy siege", "expensive")
        default_covenant.armory.add_equipment("Missle", "heavy siege", "expensive")
        default_covenant.armory.add_equipment("Missle", "heavy siege", "expensive")
        default_covenant.armory.add_equipment("Missle", "heavy siege", "expensive")
        default_covenant.armory.add_equipment("Missle", "heavy siege", "expensive")
        default_covenant.armory.add_equipment("Missle", "heavy siege", "expensive")
        default_covenant.armory.add_equipment("Missle", "heavy siege", "expensive")
        default_covenant.armory.add_equipment("Missle", "heavy siege", "expensive")
        assert default_covenant.calculate_expenditures() == 1.05


class DescribeSaveCovenant:
    @staticmethod
    def it_saves_covenant(default_covenant):
        from src.covenant import save_covenant
        default_covenant.inflation = 100
        default_covenant.covenfolken.add_covenfolk("Barg", "magi")
        default_covenant.covenfolken.add_covenfolk("le", "dependant")
        default_covenant.armory.add_equipment("earthquake machine", "heavy siege", "expensive")
        default_covenant.laboratories.add_lab("Haunted mansion Ooo")
        save_covenant(default_covenant, "cov.json")
        with open("cov.json", "r+") as f:
            cov_list = f.readlines()
            # TODO: find a better way to assert this succeeds without using load
            cov_string = cov_list[0]
            assert len(cov_list) == 1
            assert "Vernus" in cov_string


class DescribeLoadCovenant:
    @staticmethod
    def it_loads_covenant(default_covenant):
        from src.covenant import save_covenant, load_covenant_from_file
        print("DEFAULT:\n")
        print(default_covenant.armory.equipment)
        default_covenant.inflation = 100
        default_covenant.covenfolken.add_covenfolk("Barg", "magi")
        default_covenant.covenfolken.add_covenfolk("le", "dependant")
        default_covenant.armory.add_equipment("lightning machine", "heavy siege", "expensive")
        default_covenant.laboratories.add_lab("Haunted mansion Aaaa")
        save_covenant(default_covenant, "cov.json")
        loaded = load_covenant_from_file("cov.json")
        print("LOADED:\n")
        print(loaded.armory.equipment)
        assert loaded.covenfolken.covenfolk["Barg"]
        assert loaded.armory.heavy_siege["lightning machine"] == {"expensive": 1}
        assert loaded.armory.weapons["pistol"] == {}
        assert loaded.laboratories.labs["Haunted mansion Aaaa"].size == 0
        assert loaded.expenses == 9999999
