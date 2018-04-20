import re

from constants import FIND_COST, FIND_LEVEL, FIND_ENERGYCOST, FIND_DURATION, FIND_BUILDING_LINK, return_int_if_exists

# building name constants
METAL_MINE = 0
CRYSTAL_MINE = 1
DEUTERIUM_MINE = 2
SOLAR = 3
FUSION = 4
METAL_STORAGE = 5
CRYSTAL_STORAGE = 6
DEUTERIUM_STORAGE = 7
HIDDEN_METAL_STORAGE = 8
HIDDEN_CRYSTAL_STORAGE = 9
HIDDEN_DEUTERIUM_STORAGE = 10


class Building(object):
    def __init__(self, name, info_page, supply, energy_producer=False):
        self.__info_page = info_page
        self.supply = supply
        # self.category = category  # not used yet...
        self.name = name
        self.metal_cost = 0
        self.crystal_cost = 0
        self.deuterium_cost = 0
        self.level = 0
        self.__energy = 0
        self.building_time = 0
        self.upgrade_link = ''
        self.energy_producer = energy_producer
        self.refresh_info()

    @property
    def energy(self):
        if self.energy_producer:
            return self.__energy
        else:
            return self.__energy * -1

    @energy.setter
    def energy(self, energy):
        self.__energy = energy

    def extract_cost_info(self):
        extract_resource_numbers = re.findall(FIND_COST, self.__info_page.content)
        numbers = []
        for number in extract_resource_numbers:
            numbers.append(re.findall('[0-9\.]+', number)[0].replace('.', ''))
        return numbers

    def extract_level_info(self):
        extract_level = re.findall(FIND_LEVEL, self.__info_page.content)
        numbers = []
        for number in extract_level:
            numbers.append(re.findall('[0-9\.]+', number)[0].replace('.', ''))
        return return_int_if_exists(numbers, 0)

    def extract_energy_info(self):
        extract_energy = re.findall(FIND_ENERGYCOST, self.__info_page.content)
        numbers = []
        for number in extract_energy:
            numbers.append(re.findall('[0-9\.]+', number)[0].replace('.', ''))
        return return_int_if_exists(numbers, 0)

    def extract_building_time_info(self):
        extract_building_time = re.findall(FIND_DURATION, self.__info_page.content)
        build_time = 0
        for info in extract_building_time:
            i = re.findall('[0-9\.]+.{1,3}[0-9\.]*.{0,3}[0-9\.]*.{0,3}', info)
            for a in i[0].split():
                if a.endswith('s'):
                    build_time += int(a[:-1])
                elif a.endswith('m'):
                    build_time += int(a[:-1]) * 60
                elif a.endswith('h'):
                    build_time += int(a[:-1]) * 3600
        return build_time

    def get_current_upgrade_link(self, resource_page_content):
        pattern = self.supply + '.{0,1200}' + FIND_BUILDING_LINK
        link = re.findall(pattern, resource_page_content)
        try:
            final_link = re.findall('http://.{1,150}', link[0])[0][:-11]
        except IndexError:
            final_link = None
        return final_link

    def refresh_info(self, refresh_page=True):
        if refresh_page:
            self.__info_page.refresh_content()
        cost = self.extract_cost_info()
        self.metal_cost = return_int_if_exists(cost, 0)
        self.crystal_cost = return_int_if_exists(cost, 1)
        self.deuterium_cost = return_int_if_exists(cost, 2)
        self.level = self.extract_level_info()
        self.energy = self.extract_energy_info()
        self.building_time = self.extract_building_time_info()
