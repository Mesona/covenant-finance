from covenfolk import Covenfolken, Covenfolk
from covenant import Covenant
from armory import Armory
import pytest

covenfolken = {
    'magi' : 6,
    'noble' : 0,
    'companion' : 4,
    'crafter' : 0,
    'specialist': 3,
    'dependant': 0,
    'grog': 10,
    'laborer' : 0,
    'servant' : 12,
    'teamster' : 7,
    'horse': 0
}

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
        assert cov.inflation_enabled == True
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
        assert cov.inflation_enabled == False
        assert cov.inflation == 10

    @staticmethod
    def it_correctly_capitalizes_season():
        cov = Covenant(season = "WINTER")
        assert cov.season == "winter"

    @staticmethod
    def it_does_not_accept_custom_seaons():
        with pytest.raises(ValueError):
            cov = Covenant(season = "flamebroiled")

    @staticmethod
    def it_errors_when_bad_income_sources_are_added():
        with pytest.raises(TypeError):
            cov = Covenant(income_sources = {"source": "abc"})

        with pytest.raises(TypeError):
            cov = Covenant(income_sources = {1: 200})

    @staticmethod
    def it_calculates_income_source_changes():
        cov = Covenant()
        cov.advance_year()
        assert cov.treasury == 150.0
        cov.income_sources["wishing well"] = 250
        cov.advance_year()
        assert cov.treasury == 500.0

    @staticmethod
    def it_calculates_covenfolk_changes():
        cov = Covenant()
        folk = Covenfolk("george", "magi")
        cov.covenfolken.add_covenfolk(folk)
        assert cov.covenfolken.covenfolk["george"] == folk

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
        assert cov.calc_expenditures() == 5.5
        cov.change_season("autumn")
        assert cov.calc_expenditures() == 11.0

    @staticmethod
    def it_calculates_treaury_changes():
        cov = Covenant()
        cov.bank(10)
        assert cov.treasury == 60.0
        cov.bank(-100)
        assert cov.treasury == -40.0

    @staticmethod
    def it_calculates_cost_saving_changes():
        cov = Covenant()
        cov.laboratories.add_lab("route 66")
        cov.laboratories.add_lab("route 67")
        cov.laboratories.add_lab("route 68")
        cov.laboratories.add_lab("route 69")
        assert cov.calc_expenditures() == 4.0
        cov.covenfolken.add_covenfolk("worker", "crafter", "brickmaker", "laboratories", 2, "common")
        assert cov.calc_expenditures() == 5.2
        cov.covenfolken.add_covenfolk("worker 2", "crafter", "brickmaker", "laboratories", 10, "rare")
        assert cov.calc_expenditures() == 7.2

    @staticmethod
    def it_correctly_factors_cost_saving_caps_per_profession():
        cov = Covenant()
        cov.laboratories.add_lab("route 66", "aye", 5)
        assert cov.calc_expenditures() == 15.0
        cov.covenfolken.add_covenfolk("worker", "crafter", "brickmaker", "laboratories", 200, "common")
        assert cov.calc_expenditures() == 14.0

    @staticmethod
    def it_calculates_laboratory_changes():
        cov = Covenant()
        assert cov.calc_expenditures() == 0.0
        cov.laboratories.add_lab("route 66")
        assert cov.calc_expenditures() == 1.0

    @staticmethod
    def it_can_verify_too_few_teamsters_exist():
        cov = Covenant()
        cov.covenfolken.add_covenfolk("Mary", "magi")
        assert cov.meets_servant_minimum() == False
        cov.covenfolken.add_covenfolk("Todd", "servant")
        cov.covenfolken.add_covenfolk("Tammy", "servant")
        assert cov.meets_servant_minimum() == True
        
    @staticmethod
    def it_can_verify_too_few_servants_exist():
        cov = Covenant()
        cov.covenfolken.add_covenfolk("Arg", "magi")
        assert cov.meets_teamster_minimum() == False
        cov.covenfolken.add_covenfolk("Teamster", "teamster")
        assert cov.meets_teamster_minimum() == True

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

    @staticmethod
    def it_correctly_calculates_inflation():
        cov = Covenant()
        cov.inflation = 0
        assert cov.calculate_inflation(100, 200) == 2

    @staticmethod
    def it_does_not_increase_inflation_if_expenses_lowered():
        cov = Covenant()
        cov.inflation = 5
        assert cov.calculate_inflation(300, 150) == 5
