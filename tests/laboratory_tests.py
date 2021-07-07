import pytest
from laboratory import Laboratory

def demo_lab():
    lab = Laboratory(owner = "Ipsum", size = 1, virtue_points = 3, flaw_points = 2, extra_upkeep = 1, usage = "heavy")
    return lab

class DescribeLaboratories:
    @staticmethod
    def it_initializes_with_default_values():
        lab = Laboratory()
        assert lab.owner == "Lorem"
        assert lab.size == 0
        assert lab.vp == 0
        assert lab.fp == 0
        assert lab.extra_upkeep == 0
        assert lab.usage == "typical"
        assert lab.costs == 11

    @staticmethod
    def it_initializes_with_custom_values():
        lab = demo_lab()
        assert lab.owner == "Ipsum"
        assert lab.size == 1
        assert lab.vp == 3
        assert lab.fp == 2
        assert lab.extra_upkeep == 1
        assert lab.usage == "heavy"

    @staticmethod
    def it_can_set_size():
        lab = Laboratory()
        for i in range(-5, 5):
            lab.set_size(i)
            assert lab.size == i

    @staticmethod
    def it_can_increase_size():
        lab = Laboratory()
        lab.increase_size()
        assert lab.size == 1
        lab.increase_size(3)
        assert lab.size == 4

    @staticmethod
    def it_can_decrease_size():
        lab = Laboratory()
        lab.decrease_size()
        assert lab.size == -1
        lab.decrease_size(2)
        assert lab.size == -3

    @staticmethod
    def it_errors_when_lab_is_too_small():
        lab = Laboratory()
        with pytest.raises(ValueError):
            lab.set_size(-6)

        lab.set_size(-5)
        with pytest.raises(ValueError):
            lab.decrease_size()

    @staticmethod
    def it_can_change_owner():
        lab = Laboratory()
        lab.change_owner("Ipsum")
        assert lab.owner == "Ipsum"

    @staticmethod
    def it_can_add_virtue_points():
        lab = Laboratory()
        lab.add_virtue_points()
        assert lab.vp == 1
        lab.add_virtue_points(3)
        assert lab.vp == 4

    @staticmethod
    def it_can_remove_virtue_points():
        lab = Laboratory()
        lab.remove_virtue_points()
        assert lab.vp == -1
        lab.remove_virtue_points(10)
        assert lab.vp == -11

    @staticmethod
    def it_can_add_flaw_points():
        lab = Laboratory()
        lab.add_flaw_points()
        assert lab.fp == 1
        lab.add_flaw_points(5)
        assert lab.fp == 6

    @staticmethod
    def it_can_remove_flaw_points():
        lab = Laboratory()
        lab.remove_flaw_points(1)
        assert lab.fp == -1
        lab.remove_flaw_points(3)
        assert lab.fp == -4

    @staticmethod
    def it_can_set_extra_upkeep():
        lab = Laboratory()
        lab.set_extra_upkeep(5)
        assert lab.extra_upkeep == 5

    @staticmethod
    def it_has_no_default_for_set_extra_upkeep():
        lab = Laboratory()
        with pytest.raises(TypeError):
            lab.set_extra_upkeep()

    @staticmethod
    def it_can_add_extra_upkeep():
        lab = Laboratory()
        lab.add_extra_upkeep(1)
        assert lab.extra_upkeep == 1
        lab.add_extra_upkeep(4)
        assert lab.extra_upkeep == 5

    @staticmethod
    def it_can_remove_extra_upkeep():
        lab = Laboratory()
        lab.remove_extra_upkeep(1)
        assert lab.extra_upkeep == -1
        lab.remove_extra_upkeep(3)
        assert lab.extra_upkeep == -4

    @staticmethod
    def it_can_change_usage():
        lab = Laboratory()
        lab.change_usage("light")
        assert lab.usage == "light"
        lab.change_usage("heavy")
        assert lab.usage == "heavy"
        lab.change_usage("typical")
        assert lab.usage == "typical"

    @staticmethod
    def it_does_not_accept_atypical_usages():
        lab = Laboratory()
        with pytest.raises(ValueError):
            lab.change_usage("weird")

    @staticmethod
    def it_correctly_calculates_annual_costs():
        default_lab = Laboratory()
        demo = demo_lab()
        assert default_lab.costs == 11
        assert demo.costs == 46.5
        default_lab.increase_size()
        assert default_lab.costs == 16
        default_lab.add_extra_upkeep()
        assert default_lab.costs == 31

