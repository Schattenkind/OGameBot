import game


class QueuedBuilding(object):
    def __init__(self, building, level):
        self.name = building.name
        self.building = building
        self.base_metal_cost = 0
        self.base_crystal_cost = 0
        self.base_deuterium_cost = 0
        self.level = level

    @property
    def building_time(self, robotics_level=0, naniten_level=0):
        if (4 - self.level / 2) <= 1:
            x = 1
        else:
            x = 4 - self.level / 2
        '''return int(((self.metal_cost + self.crystal_cost) /
                    (2500 * (1 + robotics_level) * (2 ** naniten_level) * game.Game.UNIVERSE_SPEED)) * 3600)'''
        return ((self.metal_cost + self.crystal_cost) * 1.44 / x / (
            1 + robotics_level) / 2 ** naniten_level / game.Game.UNIVERSE_SPEED)

    @property
    def metal_cost(self):
        return int(self.base_metal_cost * 2 ** (self.level - 1))

    @property
    def crystal_cost(self):
        return int(self.base_crystal_cost * 2 ** (self.level - 1))

    @property
    def deuterium_cost(self):
        return int(self.base_crystal_cost * 2 ** (self.level - 1))

    @property
    def energy(self):
        return int(10 * self.level * 1.1 ** (self.level - 1))


class QMetalMine(QueuedBuilding):
    def __init__(self, building, level):
        super().__init__(building, level)
        self.base_metal_cost = 60
        self.base_crystal_cost = 15

    @property
    def metal_cost(self):
        return int(self.base_metal_cost * 1.5 ** (self.level - 1))

    @property
    def crystal_cost(self):
        return int(self.base_crystal_cost * 1.5 ** (self.level - 1))


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
    def metal_cost(self):
        return int(self.base_metal_cost * 1.5 ** (self.level - 1))

    @property
    def crystal_cost(self):
        return int(self.base_crystal_cost * 1.5 ** (self.level - 1))

    @property
    def energy(self):
        return int(20 * self.level * 1.1 ** (self.level - 1))


class QSolar(QueuedBuilding):
    def __init__(self, building, level):
        super().__init__(building, level)
        self.base_metal_cost = 75
        self.base_crystal_cost = 30

    @property
    def metal_cost(self):
        return int(self.base_metal_cost * 1.5 ** (self.level - 1))

    @property
    def crystal_cost(self):
        return int(self.base_crystal_cost * 1.5 ** (self.level - 1))

    @property
    def energy(self):
        return int(20 * self.level * 1.1 ** (self.level - 1))


class QFusion(QueuedBuilding):
    def __init__(self, building, level):
        super().__init__(building, level)
        self.base_metal_cost = 900
        self.base_crystal_cost = 360
        self.base_deuterium_cost = 180

    @property
    def metal_cost(self):
        return self.base_metal_cost * 1.8 ** (self.level - 1)

    @property
    def crystal_cost(self):
        return self.base_crystal_cost * 1.8 ** (self.level - 1)

    @property
    def deuterium_cost(self):
        return self.base_deuterium_cost * 1.8 ** (self.level - 1)

    @property
    def energy(self):
        return int(20 * self.level * 1.1 ** (self.level - 1))


class QMetallStorage(QueuedBuilding):
    def __init__(self, building, level):
        super().__init__(building, level)
        self.base_metal_cost = 1000

    @property
    def energy(self):
        return 0


class QKrystalStorage(QueuedBuilding):
    def __init__(self, building, level):
        super().__init__(building, level)
        self.base_metal_cost = 1000
        self.base_crystal_cost = 500

    @property
    def energy(self):
        return 0


class QDeuteriumStorage(QueuedBuilding):
    def __init__(self, building, level):
        super().__init__(building, level)
        self.base_metal_cost = 1000
        self.base_crystal_cost = 1000

    @property
    def energy(self):
        return 0
