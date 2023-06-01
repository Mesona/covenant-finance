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
    cov = semita()

    yield cov

    cov.delete_covenant()

def custom_covenant():
    cov = Covenant(
            name = "Lorem",
            season = "autumn",
            income_sources = {"source": 250, "source2": 100},
            tithes = {"Lord Farqua": 10},
            treasury = 75.5,
            laboratories = {},
            inflation_enabled = False,
            inflation = 10,
    )
    return cov

class DescribeCovenant:
    @staticmethod
    def it_initializes_with_default_values():
        cov = Covenant()
        assert cov.name == "Vernus"
        assert cov.season == "spring"
        assert cov.income_sources == {"source": 100}
        assert cov.tithes == {}
        assert cov.treasury == 50.0
        assert cov.covenfolken.covenfolk == {}
        assert cov.laboratories.labs == {}
        assert isinstance(cov.armory, Armory)
        assert cov.inflation_enabled is True
        assert cov.inflation == 0

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

    # FIXME: These 2 tests cause env bleed
    @staticmethod
    def it_can_initialize_semita(set_and_clean_up_semita):
        assert set_and_clean_up_semita

    @staticmethod
    def it_calculates_semita_servant_requirements_same_as_book(set_and_clean_up_semita):
        assert set_and_clean_up_semita.calculate_servant_minimum() == 16

    @staticmethod
    def it_calculates_semita_teamster_requirements_same_as_book(set_and_clean_up_semita):
        assert set_and_clean_up_semita.calculate_teamster_minimum() == 4

    @staticmethod
    def it_correctly_capitalizes_season():
        cov = Covenant(season = "WINTER")
        assert cov.season == "winter"
        cov.delete_covenant()

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
    def it_calculates_income_source_changes():
        cov = Covenant()
        cov.advance_year()
        assert cov.treasury == 150.0
        cov.income_sources["wishing well"] = 250
        cov.advance_year()
        assert cov.treasury == 500.0
        cov.delete_covenant()

    @staticmethod
    def it_calculates_covenfolk_changes():
        cov = Covenant()
        folk = Covenfolk("george", "magi")
        cov.covenfolken.add_covenfolk(folk)
        assert cov.covenfolken.covenfolk["george"] == folk
        cov.delete_covenant()

    @staticmethod
    def it_can_change_seasons():
        cov = Covenant()
        cov.change_season("autumn")
        assert cov.season == "autumn"

    @staticmethod
    def it_calculates_season_changes():
        cov = Covenant()
        folk = Covenfolk("george", "magi")
        cov.covenfolken.add_covenfolk(folk)
        assert cov.calculate_expenditures() == 5.5
        cov.change_season("autumn")
        assert cov.calculate_expenditures() == 11.0

    @staticmethod
    def it_calculates_treaury_changes():
        cov = Covenant()
        cov.bank(10)
        assert cov.treasury == 60.0
        cov.bank(-100)
        assert cov.treasury == -40.0
        cov.delete_covenant()

    @staticmethod
    def it_calculates_lab_cost_saving_changes():
        cov = Covenant()
        cov.laboratories.add_lab("route 66")
        cov.laboratories.add_lab("route 67")
        cov.laboratories.add_lab("route 68")
        cov.laboratories.add_lab("route 69")
        assert cov.calculate_expenditures() == 4.0
        cov.covenfolken.add_covenfolk("worker", "crafter", "brickmaker", "laboratories", 2, "common")
        assert cov.calculate_expenditures() == 5.2
        cov.covenfolken.add_covenfolk("worker 2", "crafter", "brickmaker", "laboratories", 10, "rare")
        assert cov.calculate_expenditures() == 7.2
        cov.delete_covenant()

    @staticmethod
    def it_correctly_factors_cost_saving_caps_per_profession():
        cov = Covenant()
        cov.laboratories.add_lab("route 66", "aye", 5)
        assert cov.calculate_expenditures() == 15.0
        cov.covenfolken.add_covenfolk("worker", "crafter", "brickmaker", "laboratories", 200, "common")
        assert cov.calculate_expenditures() == 14.0
        cov.delete_covenant()

    @staticmethod
    def it_calculates_laboratory_changes():
        cov = Covenant()
        assert cov.calculate_expenditures() == 0.0
        cov.laboratories.add_lab("route 66")
        assert cov.calculate_expenditures() == 1.0
        cov.delete_covenant()

    @staticmethod
    def it_can_verify_too_few_teamsters_exist():
        cov = Covenant()
        cov.covenfolken.add_covenfolk("Mary", "magi")
        assert cov.meets_laborer_minimum() == False
        cov.covenfolken.add_covenfolk("Todd", "laborer")
        cov.covenfolken.add_covenfolk("Tammy", "laborer")
        assert cov.meets_laborer_minimum() == True
        cov.delete_covenant()
        
    @staticmethod
    def it_can_verify_too_few_laborers_exist():
        cov = Covenant()
        cov.covenfolken.add_covenfolk("Arg", "magi")
        assert cov.meets_teamster_minimum() == False
        cov.covenfolken.add_covenfolk("Teamster", "teamster")
        assert cov.meets_teamster_minimum() == True
        cov.delete_covenant()

    @staticmethod
    def it_correctly_factors_in_laborers_for_teamster_requirements():
        cov = Covenant()
        cov.covenfolken.add_covenfolk("Arg", "magi")
        cov.covenfolken.add_covenfolk("gle", "magi")
        cov.covenfolken.add_covenfolk("Barg", "magi")
        assert cov.meets_teamster_minimum() == False
        cov.covenfolken.add_covenfolk("le", "dependant")
        cov.covenfolken.add_covenfolk("woo", "dependant")
        cov.covenfolken.add_covenfolk("tem", "teamster")
        assert cov.meets_teamster_minimum() == False
        cov.covenfolken.add_covenfolk("lab", "laborer")
        cov.covenfolken.add_covenfolk("orer", "laborer")
        assert cov.meets_teamster_minimum() == False
        cov.delete_covenant()

    @staticmethod
    def it_correctly_calculates_inflation():
        cov = Covenant()
        cov.inflation = 0
        assert cov.calculate_inflation(100, 200) == 2
        cov.delete_covenant()

    @staticmethod
    def it_does_not_increase_inflation_if_expenses_lowered():
        cov = Covenant()
        cov.inflation = 5
        assert cov.calculate_inflation(300, 150) == 5
        cov.delete_covenant()

    @staticmethod
    def it_calculates_armory_increases():
        cov = Covenant()
        cov.armory.add_equipment("sword", "weapon", "expensive")
        assert cov.calculate_expenditures() == 0.05
        cov.armory.add_equipment("Missle", "heavy siege", "expensive")
        cov.armory.add_equipment("Missle", "heavy siege", "expensive")
        cov.armory.add_equipment("Missle", "heavy siege", "expensive")
        cov.armory.add_equipment("Missle", "heavy siege", "expensive")
        cov.armory.add_equipment("Missle", "heavy siege", "expensive")
        cov.armory.add_equipment("Missle", "heavy siege", "expensive")
        cov.armory.add_equipment("Missle", "heavy siege", "expensive")
        cov.armory.add_equipment("Missle", "heavy siege", "expensive")
        cov.armory.add_equipment("Missle", "heavy siege", "expensive")
        cov.armory.add_equipment("Missle", "heavy siege", "expensive")
        assert cov.calculate_expenditures() == 1.05
        cov.delete_covenant()


class DescribeSaveCovenant:
    @staticmethod
    def it_saves_covenant():
        from src.covenant import save_covenant
        cov = Covenant()
        cov.inflation = 100
        cov.covenfolken.add_covenfolk("Barg", "magi")
        cov.covenfolken.add_covenfolk("le", "dependant")
        cov.armory.add_equipment("earthquake machine", "heavy siege", "expensive")
        cov.laboratories.add_lab("Haunted mansion Ooo")
        save_covenant(cov, "cov.json")
        with open("cov.json", "r+") as f:
            cov_list = f.readlines()
            # TODO: find a better way to assert this succeeds without using load
            cov_string = cov_list[0]
            assert len(cov_list) == 1
            assert "Vernus" in cov_string
        cov.delete_covenant()


class DescribeLoadCovenant:
    @staticmethod
    def it_loads_covenant():
        from src.covenant import save_covenant, load_covenant_from_file
        cov = Covenant()
        cov.inflation = 100
        cov.covenfolken.add_covenfolk("Barg", "magi")
        cov.covenfolken.add_covenfolk("le", "dependant")
        cov.armory.add_equipment("earthquake machine", "heavy siege", "expensive")
        cov.laboratories.add_lab("Haunted mansion Aaaa")
        save_covenant(cov, "cov.json")
        loaded = load_covenant_from_file("cov.json")
        assert loaded.covenfolken.covenfolk["Barg"]
        assert loaded.armory.heavy_siege["earthquake machine"] == {"expensive": 1}
        assert loaded.armory.weapons["pistol"] == {}
        assert loaded.laboratories.labs["Haunted mansion"].size == 0
        assert loaded.expenses == 9999999
        cov.delete_covenant()
