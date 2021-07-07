class Laboratory:
    def __init__(self, owner="Lorem", size=0, virtue_points=0, flaw_points=0, extra_upkeep=0, usage="typical"):
        self.owner = owner
        self.size = size
        self.vp = virtue_points
        self.fp = flaw_points
        self.extra_upkeep = extra_upkeep
        self.usage = usage
        self.costs = self.calculate_annual_costs()

    def set_size(self, size):
        if size < -5:
            raise ValueError("Laboratories cannot be smaller than size -5")

        self.size = size 
        self.costs = self.calculate_annual_costs()

    def increase_size(self, size=1):
        self.size += size
        self.costs = self.calculate_annual_costs()

    def decrease_size(self, size=1):
        new_size = self.size - size
        if new_size <= -5:
            raise ValueError("Laboratories cannot be smaller than size -5")

        self.size = new_size
        self.costs = self.calculate_annual_costs()

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
        self.costs = self.calculate_annual_costs()

    def add_extra_upkeep(self, upkeep=1):
        self.extra_upkeep += upkeep
        self.costs = self.calculate_annual_costs()

    def remove_extra_upkeep(self, upkeep=1):
        self.extra_upkeep -= upkeep
        self.costs = self.calculate_annual_costs()

    def change_usage(self, usage):
        if not usage.lower() in ["light", "typical", "heavy"]:
            raise ValueError("Usage can only be 'light', 'typical', or 'heavy'")

        self.usage = usage.lower()
        self.costs = self.calculate_annual_costs()

    def calculate_annual_costs(self):
        upkeep_multiplier = 0
        if self.usage == "light":
            upkeep_multiplier = 0.5
        elif self.usage == "typical":
            upkeep_multiplier = 1
        elif self.usage == "heavy":
            upkeep_multiplier = 1.5

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

        base_costs = 1

        print("EXTRA UPKEEP:", self.extra_upkeep)
        total_costs = (base_lab_points[self.size + self.extra_upkeep] + base_costs) * upkeep_multiplier
        return total_costs
