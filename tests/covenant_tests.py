from covenfolk import Covenfolken
from covenant import Covenant
import pytest

covenfolken = {
    'magi' : 6,
    'nobles' : 0,
    'companions' : 4,
    'crafters' : 0,
    'specialists': 3,
    'dependants': 0,
    'grogs': 10,
    'laborers' : 0,
    'servants' : 12,
    'teamsters' : 7,
    'horses': 0
}

def custom_covenant():
    cov = Covenant(
            name = "Lorem",
            season = "fall",
            income_sources = {"source": 250, "source2": 100},
            tithes = {"Lord Farqua": 10},
            treasury = 75.5,
            covenfolken = Covenfolken(),
            laboratories = {},
            armory = 5,
            inflation_enabled = False,
            inflation_value = 10,
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
        assert cov.laboratories == {}
        #assert cov.armory == cov.covenfolken['grogs'] * 32
        assert cov.inflation_enabled == True
        assert cov.inflation == 0

    @staticmethod
    def it_initializes_with_custom_values():
        cov = custom_covenant()
        assert cov.name == "Lorem"
        assert cov.season == "fall"
        assert cov.income_sources == {"source": 250, "source2": 100}
        assert cov.tithes == {"Lord Farqua": 10}
        assert cov.treasury == 75.5
        assert cov.covenfolken.covenfolk == {}
        assert cov.armory == 5
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
        pass

    @staticmethod
    def it_calculates_covenfolk_changes():
        pass

    @staticmethod
    def it_can_change_seasons():
        pass

    @staticmethod
    def it_calculates_season_changes():
        pass

    @staticmethod
    def it_calculates_treaury_changes():
        pass

    @staticmethod
    def it_calculates_cost_saving_changes():
        pass

    @staticmethod
    def it_calculates_laboratory_changes():
        pass

    @staticmethod
    def it_errors_when_too_few_teamsters_exist():
      pass

    @staticmethod
    def it_errors_when_too_few_servants_exist():
      pass
