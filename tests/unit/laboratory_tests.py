import pytest
from src.laboratory import Laboratory, Laboratories

def demo_lab():
    lab = Laboratory(
            name = "mountaintop 1",
            owner = "Ipsum",
            size = 1,
            virtue_points = 3,
            flaw_points = 2,
            extra_upkeep = 1,
            usage = "heavy",
            minor_fortifications = 1,
            major_fortifications = 2,
    )
    return lab

class DescribeLaboratories:
    @staticmethod
    def it_initializes():
        from collections import defaultdict
        labs = Laboratories()
        assert isinstance(labs.labs, defaultdict)

    @staticmethod
    def it_adds_lab_objects():
        lab = demo_lab()
        labs = Laboratories()
        labs.add_lab(lab)
        assert labs.labs[lab.name] == lab

    @staticmethod
    def it_adds_lab_by_passing_parameters():
        labs = Laboratories()
        labs.add_lab("seaside manor", "Oopsie", 1, 4, 5, 6, "heavy", 1, 2)
        assert labs.labs["seaside manor"] != False
        assert labs.labs["seaside manor"].owner == "Oopsie"
        assert labs.labs["seaside manor"].size == 1
        assert labs.labs["seaside manor"].usage == "heavy"

    @staticmethod
    def it_removes_labs():
        lab = demo_lab()
        labs = Laboratories()
        labs.add_lab(lab)
        assert labs.labs[lab.name] == lab
        labs.remove_lab("mountaintop 1")
        assert len(labs.labs.keys()) == 0

    @staticmethod
    def it_vaidates_unique_names():
        lab = demo_lab()
        labs = Laboratories()
        labs.add_lab(lab)
        with pytest.raises(ValueError):
            labs.add_lab(lab)

    @staticmethod
    def it_calculates_total_point_costs():
        lab = demo_lab()
        labs = Laboratories()
        labs.add_lab("seaside manor", "Oopsie", 1, 4, 5, 6, "heavy", 1, 2)
        assert labs.calculate_total_point_costs() == 420.0
        labs.add_lab(lab)
        assert labs.calculate_total_point_costs() == 465.0


class DescribeLaboratory:
    @staticmethod
    def it_initializes_with_default_values():
        lab = Laboratory(name="faerie garden")
        assert lab.name == "faerie garden"
        assert lab.owner == ""
        assert lab.size == 0
        assert lab.vp == 0
        assert lab.fp == 0
        assert lab.extra_upkeep == 0
        assert lab.usage == "typical"
        assert lab.points == 10
        assert lab.minor_fortifications == 0
        assert lab.major_fortifications == 0

    @staticmethod
    def it_initializes_with_custom_values():
        lab = demo_lab()
        assert lab.name == "mountaintop 1"
        assert lab.owner == "Ipsum"
        assert lab.size == 1
        assert lab.vp == 3
        assert lab.fp == 2
        assert lab.extra_upkeep == 1
        assert lab.usage == "heavy"
        assert lab.minor_fortifications == 1
        assert lab.major_fortifications == 2

    @staticmethod
    def it_can_set_size():
        lab = Laboratory("apprentice lab")
        for i in range(-5, 5):
            lab.set_size(i)
            assert lab.size == i

    @staticmethod
    def it_can_increase_size():
        lab = Laboratory("apprentice lab")
        lab.increase_size()
        assert lab.size == 1
        lab.increase_size(3)
        assert lab.size == 4

    @staticmethod
    def it_can_decrease_size():
        lab = Laboratory("apprentice lab")
        lab.decrease_size()
        assert lab.size == -1
        lab.decrease_size(2)
        assert lab.size == -3

    @staticmethod
    def it_errors_when_lab_is_too_small():
        lab = Laboratory("apprentice lab")
        with pytest.raises(ValueError):
            lab.set_size(-6)

        lab.set_size(-5)
        with pytest.raises(ValueError):
            lab.decrease_size()

    @staticmethod
    def it_can_change_owner():
        lab = Laboratory("apprentice lab")
        lab.change_owner("Ipsum")
        assert lab.owner == "Ipsum"

    @staticmethod
    def it_can_add_virtue_points():
        lab = Laboratory("apprentice lab")
        lab.add_virtue_points()
        assert lab.vp == 1
        lab.add_virtue_points(3)
        assert lab.vp == 4

    @staticmethod
    def it_can_remove_virtue_points():
        lab = Laboratory("apprentice lab")
        lab.remove_virtue_points()
        assert lab.vp == -1
        lab.remove_virtue_points(10)
        assert lab.vp == -11

    @staticmethod
    def it_can_add_flaw_points():
        lab = Laboratory("apprentice lab")
        lab.add_flaw_points()
        assert lab.fp == 1
        lab.add_flaw_points(5)
        assert lab.fp == 6

    @staticmethod
    def it_can_remove_flaw_points():
        lab = Laboratory("apprentice lab")
        lab.remove_flaw_points(1)
        assert lab.fp == -1
        lab.remove_flaw_points(3)
        assert lab.fp == -4

    @staticmethod
    def it_can_set_extra_upkeep():
        lab = Laboratory("apprentice lab")
        lab.set_extra_upkeep(5)
        assert lab.extra_upkeep == 5

    @staticmethod
    def it_has_no_default_for_set_extra_upkeep():
        lab = Laboratory("apprentice lab")
        with pytest.raises(TypeError):
            lab.set_extra_upkeep()

    @staticmethod
    def it_can_add_extra_upkeep():
        lab = Laboratory("apprentice lab")
        lab.add_extra_upkeep(1)
        assert lab.extra_upkeep == 1
        lab.add_extra_upkeep(4)
        assert lab.extra_upkeep == 5

    @staticmethod
    def it_can_remove_extra_upkeep():
        lab = Laboratory("apprentice lab")
        lab.remove_extra_upkeep(1)
        assert lab.extra_upkeep == -1
        lab.remove_extra_upkeep(3)
        assert lab.extra_upkeep == -4

    @staticmethod
    def it_can_change_usage():
        lab = Laboratory("apprentice lab")
        lab.change_usage("light")
        assert lab.usage == "light"
        lab.change_usage("heavy")
        assert lab.usage == "heavy"
        lab.change_usage("typical")
        assert lab.usage == "typical"

    @staticmethod
    def it_does_not_accept_atypical_usages():
        lab = Laboratory("apprentice lab")
        with pytest.raises(ValueError):
            lab.change_usage("weird")

    @staticmethod
    def it_correctly_calculates_annual_points():
        default_lab = Laboratory("apprentice lab")
        demo = demo_lab()
        assert default_lab.points == 10
        assert demo.points == 45.0
        default_lab.increase_size()
        assert default_lab.points == 15
        default_lab.add_extra_upkeep()
        assert default_lab.points == 30

    @staticmethod
    def it_correctly_adds_minor_fortifications():
        lab = Laboratory("apprentice lab")
        lab.add_minor_fortification()
        assert lab.minor_fortifications == 1
        lab.add_minor_fortification(3)
        assert lab.minor_fortifications == 4

    @staticmethod
    def it_correctly_removes_minor_fortifications():
        lab = Laboratory("test lab", minor_fortifications = 10)
        lab.remove_minor_fortification()
        assert lab.minor_fortifications == 9
        lab.remove_minor_fortification(6)
        assert lab.minor_fortifications == 3

    @staticmethod
    def it_correctly_adds_major_fortifications():
        lab = Laboratory("apprentice lab")
        lab.add_major_fortification()
        assert lab.major_fortifications == 1
        lab.add_major_fortification(2)
        assert lab.major_fortifications == 3

    @staticmethod
    def it_correctly_removes_major_fortifications():
        lab = Laboratory("test lab", major_fortifications = 10)
        lab.remove_major_fortification()
        assert lab.major_fortifications == 9
        lab.remove_major_fortification(5)
        assert lab.major_fortifications == 4

    @staticmethod
    def it_correctly_raises_errors_when_too_few_minor_fortifications():
        lab = Laboratory("apprentice lab")
        with pytest.raises(ValueError):
            lab.remove_minor_fortification()

    @staticmethod
    def it_correctly_raises_errors_when_too_few_major_fortifications():
        lab = Laboratory("apprentice lab")
        with pytest.raises(ValueError):
            lab.remove_major_fortification()

    @staticmethod
    def it_correctly_changes_name():
        lab = Laboratory("apprentice lab")
        lab.change_name("crater")
        assert lab.name == "crater"
