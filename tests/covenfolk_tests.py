import pytest
from covenfolk import Covenfolken, Covenfolk, validate_classification, validate_saving_category

def demo_folk():
    return Covenfolk(name="Jimmy", classification="crafter")

class DescribeCovenfolk:
    @staticmethod
    def it_initializes_with_default_values():
        folk = demo_folk()
        assert folk.name == "Jimmy"
        assert folk.classification == "crafter"
        assert folk.saving_category == ""
        assert folk.skill == 0

    @staticmethod
    def it_accepts_inputs():
        folk = Covenfolk(name="A", classification="noble", saving_category="buildings", skill=1)
        assert folk.name == "A"
        assert folk.classification == "noble"
        assert folk.saving_category == "buildings"
        assert folk.skill == 1

    @staticmethod
    def it_raises_error_with_incorrect_saving_category():
        with pytest.raises(ValueError):
            folk = Covenfolk(name="A", classification="noble", saving_category="Gong Farmer", skill=99)

    @staticmethod
    def it_sets_skill_level_properly():
        folk = demo_folk()
        folk.set_skill(23)
        assert folk.skill == 23
        folk.set_skill(4)
        assert folk.skill == 4

    @staticmethod
    def it_increases_skill_levels():
        folk = demo_folk()
        folk.increase_skill()
        assert folk.skill == 1
        folk.increase_skill(4)
        assert folk.skill == 5

    @staticmethod
    def it_reduces_skill_levels():
        folk = demo_folk()
        folk.set_skill(50)
        folk.reduce_skill()
        assert folk.skill == 49
        folk.reduce_skill(10)
        assert folk.skill == 39

    @staticmethod
    def it_changes_name():
        folk = demo_folk()
        folk.change_name("ABC")
        assert folk.name == "ABC"

    @staticmethod
    def it_raises_errors_if_skill_below_zero():
        folk = demo_folk()
        with pytest.raises(ValueError):
            folk.reduce_skill(5)

    @staticmethod
    def it_raises_errors_if_created_with_negative_skills():
        with pytest.raises(ValueError):
            folk = Covenfolk(name="a", classification="mage", skill = -5)

    @staticmethod
    def it_raises_errors_if_created_with_bad_classification():
        with pytest.raises(ValueError):
            folk = Covenfolk(name="a", classification="Floor licker")


class DescribeValidateProfession:
    @staticmethod
    def it_accepts_known_classification():
        classifications = [
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

        for classification in classifications:
            validate_classification(classification)

    @staticmethod
    def it_errors_on_unknown_classifications():
        with pytest.raises(ValueError):
            validate_classification("daydreamer")


class DescribeValidateSavingCategory:
    @staticmethod
    def it_accepts_known_saving_categories():
        categories = [
                "buildings",
                "consumables",
                "laboratories",
                "provisions",
                "weapons and armor",
                "writing materials",
        ]

        for category in categories:
            validate_saving_category(category)

    @staticmethod
    def it_raises_error_with_invalid_categories():
        with pytest.raises(ValueError):
            validate_saving_category("Flower picker")


class DescribeCovenfolken:
    @staticmethod
    def it_instantiates():
        cn = Covenfolken()
        assert cn == {}

    def it_accepts_new_covenfolk():
        cn = Covenfolken()
        folk = demo_folk()
        cn.add_covenfolk

