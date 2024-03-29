import pytest
from src.covenfolk import Covenfolken, Covenfolk, validate_classification, validate_saving_category

def demo_folk():
    return Covenfolk(
            name="Jimmy",
            classification="crafter",
            profession="woodworker",
            saving_category="buildings",
            rarity="common",
    )

class DescribeCovenfolk:
    @staticmethod
    def it_initializes_with_default_values():
        folk = Covenfolk("Jimmy", "laborer")
        assert folk.name == "Jimmy"
        assert folk.classification == "laborer"
        assert folk.saving_category == "provisions"
        assert folk.profession == ""
        assert folk.skill == 0
        assert folk.rarity == ""

    @staticmethod
    def it_accepts_inputs():
        folk = Covenfolk(name="A", classification="noble", saving_category="buildings", skill=1)
        assert folk.name == "A"
        assert folk.classification == "noble"
        assert folk.saving_category == "buildings"
        assert folk.skill == 1

    @staticmethod
    def it_requires_saving_category_for_crafters():
        with pytest.raises(ValueError):
            folk = Covenfolk(
                    name="a",
                    classification="crafter",
                    profession="smith",
                    skill=5,
                    rarity="common",
            )

    @staticmethod
    def it_automatically_assigns_savings_category_for_laborers():
        folk = Covenfolk(name="a", classification="laborer")
        assert folk.saving_category == "provisions"

    @staticmethod
    def it_requires_professions_for_crafters():
        with pytest.raises(ValueError):
            folk = Covenfolk(
                    name="a",
                    classification="crafter",
                    saving_category="weapons and armor",
                    skill=5,
                    rarity="common",
            )

    @staticmethod
    def it_requires_rarity_for_crafters():
        with pytest.raises(ValueError):
            folk = Covenfolk(
                    name="a",
                    classification="crafter",
                    profession="smith",
                    saving_category="weapons and armor",
                    skill=5,
            )

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
            folk = Covenfolk(name="a", classification="magi", skill = -5)

    @staticmethod
    def it_raises_errors_if_created_with_bad_classification():
        with pytest.raises(ValueError):
            folk = Covenfolk(name="a", classification="Floor licker")


class DescribeValidateProfession:
    @staticmethod
    def it_accepts_known_classification():
        classifications = [
                "magi",
                "noble",
                "companion",
                "crafter",
                "specialist",
                "dependant",
                "grog",
                "laborer",
                "laborer",
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
                "writing",
        ]

        for category in categories:
            validate_saving_category(category)

    @staticmethod
    def it_raises_error_with_invalid_categories():
        with pytest.raises(ValueError):
            validate_saving_category("Flower picker")


class DescribeCovenfolken:
    @staticmethod
    def it_calculates_the_savings_of_all_its_covenfolk():
        cn = Covenfolken()
        folk = demo_folk()
        cn.add_covenfolk(folk)
        cn.add_covenfolk("James", "crafter", "woodworker", "buildings", 3, "common")
        cn.add_covenfolk("Arc", "crafter", "welder", "weapons and armor", 5, "rare")
        savings = cn.calculate_all_savings()
        assert savings["buildings"]["woodworker"] == 3
        assert savings["weapons and armor"]["welder"] == 6

    @staticmethod
    def it_calculates_the_savings_of_one_category():
        cn = Covenfolken()
        folk = demo_folk()
        cn.add_covenfolk(folk)
        assert cn.calculate_savings_of("buildings") == {"woodworker": 1}
        cn.add_covenfolk("James", "crafter", "woodworker", "buildings", 3, "common")
        assert cn.calculate_savings_of("buildings") == {"woodworker": 3}
        cn.add_covenfolk("Arc", "crafter", "welder", "weapons and armor", 5, "rare")
        assert cn.calculate_savings_of("weapons and armor") == {"welder": 6}

    @staticmethod
    def it_instantiates():
        cn = Covenfolken()
        assert cn.covenfolk == {}

    @staticmethod
    def it_accepts_new_covenfolk_objects():
        cn = Covenfolken()
        folk = demo_folk()
        cn.add_covenfolk(folk)
        assert folk in cn.covenfolk.values()

    @staticmethod
    def it_creates_new_covenfolk_when_passed_parameters():
        cn = Covenfolken()
        cn.add_covenfolk("jane", "magi")
        assert "jane" in cn.covenfolk.keys()
        assert isinstance(cn.covenfolk["jane"], Covenfolk)

    @staticmethod
    def it_removes_covenfolk():
        cn = Covenfolken()
        folk = demo_folk()
        cn.add_covenfolk(folk)
        assert folk in cn.covenfolk.values()
        cn.remove_covenfolk(folk.name)
        assert folk not in cn.covenfolk.values()

    @staticmethod
    def it_displays_covenfolk(capsys):
        cn = Covenfolken()
        cn.add_covenfolk("weber", "magi")
        cn.add_covenfolk("a", "magi", "writer", "consumables", 5)
        cn.display_covenfolk()
        captured = capsys.readouterr()
        assert captured.out == """weber: magi

a: magi
Savings Category: consumables
writer: 5

"""

    @staticmethod
    def it_lists_covenfolk_names(capsys):
        cn = Covenfolken()
        cn.add_covenfolk("weber", "magi")
        cn.add_covenfolk("yawgma", "magi")
        cn.list()
        captured = capsys.readouterr()
        assert captured.out == "['weber', 'yawgma']\n"

    @staticmethod
    def it_returns_the_total_number_of_covenfolk_matching_classification():
        cn = Covenfolken()
        cn.add_covenfolk("weber", "magi", "writer", "consumables", 10)
        cn.add_covenfolk("yawgma", "magi", "hammerer", "buildings", 5)
        cn.add_covenfolk("dog", "horse", "stables", "buildings", 2)
        assert cn.total_count_of("magi") == 2
        assert cn.total_count_of("horse") == 1
        assert isinstance(cn.total_count_of("magi"), int)

    @staticmethod
    def it_returns_the_total_number_of_covenfolk_matching_profession():
        cn = Covenfolken()
        cn.add_covenfolk("weber", "magi", "writer", "consumables", 10)
        cn.add_covenfolk("yawgma", "magi", "hammerer", "buildings", 5)
        cn.add_covenfolk("dog", "horse", "stables", "buildings", 2)
        assert cn.total_count_of("writer") == 1
