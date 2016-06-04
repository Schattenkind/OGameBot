from constants import UNIVERSE_SPEED


class QueuedBuilding(object):
    def __init__(self, building, level):
        self.name = building.name
        self.building = building
        self.base_metal_cost = 0
        self.base_crystal_cost = 0
        self.deuterium_cost = 0
        self.level = level

    @property
    def building_time(self, robotics_level=0, naniten_level=0):
        if 4 - self.level / 2 > 1:
            x = 4 - self.level / 2
        else:
            x = 1
        return int(((self.metal_cost + self.crystal_cost) * 1.44 / x / (
            1 + robotics_level) / 2 ** naniten_level) / UNIVERSE_SPEED) + 1

    @property
    def metal_cost(self):
        return int(self.base_metal_cost * 1.5 ** (self.level - 1))

    @property
    def crystal_cost(self):
        return int(self.base_crystal_cost * 1.5 ** (self.level - 1))

    @property
    def energy(self):
        return int(10 * self.level * 1.1 ** (self.level - 1))


class QMetalMine(QueuedBuilding):
    def __init__(self, building, level):
        super().__init__(building, level)
        self.base_metal_cost = 60
        self.base_crystal_cost = 15


class QCrystalMine(QueuedBuilding):
    def __init__(self, building, level):
        super().__init__(building, level)
        self.base_metal_cost = 48
        self.base_crystal_cost = 24

    @property
    def metal_cost(self):
        return int(self.base_metal_cost * 1.6 ** (self.level - 1))

    @property
    def crystal_cost(self):
        return int(self.base_crystal_cost * 1.6 ** (self.level - 1))


class QDeuteriumMine(QueuedBuilding):
    def __init__(self, building, level):
        super().__init__(building, level)
        self.base_metal_cost = 225
        self.base_crystal_cost = 75

    @property
    def energy(self):
        return int(20 * self.level * 1.1 ** (self.level - 1))


class QSolar(QueuedBuilding):
    def __init__(self, building, level):
        super().__init__(building, level)
        self.base_metal_cost = 75
        self.base_crystal_cost = 30

    @property
    def energy(self):
        return int(20 * self.level * 1.1 ** (self.level - 1))
