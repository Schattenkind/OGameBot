from buildings.queued_building import *
from constants import *

import re
import time
import threading


class Queue(threading.Thread):
    def __init__(self, planet):
        threading.Thread.__init__(self, daemon=True)
        self.planet = planet
        self.buildings_queue = []
        self.current_remaining_time = 0
        self.stop = False

    def add_to_queue(self, building):
        level = building.level + 1 + self.currently_queued_buildings_with_name(building.name)
        if building.supply == 'supply1':
            queue_item = QMetalMine(building, level)
            self.buildings_queue.append(queue_item)
        elif building.supply == 'supply2':
            queue_item = QCrystalMine(building, level)
            self.buildings_queue.append(queue_item)
        elif building.supply == 'supply3':
            queue_item = QDeuteriumMine(building, level)
            self.buildings_queue.append(queue_item)
        elif building.supply == 'supply4':
            queue_item = QSolar(building, level)
            self.buildings_queue.append(queue_item)
        else:
            queue_item = QueuedBuilding(building, level)
            self.buildings_queue.append(queue_item)
        return queue_item

    def upgrade_building(self, building_queue_item):
        """
        :param building_queue_item: queue item to upgrade
        :return: 0 - building is successfully upgrading
                 1 - not enough materials
                 2 - other reason why it could not be upgraded (e.g. other building still being build)
        """
        building = None
        for b in self.planet.building.keys():
            if self.planet.building[b].name == building_queue_item.name:
                building = self.planet.building[b]
        self.planet.page['resource'].refresh_content()
        if self.planet.resource['metal'].actual < building.metal_cost:
            return 1
        if self.planet.resource['crystal'].actual < building.crystal_cost:
            return 1
        if self.planet.resource['deuterium'].actual < building.deuterium_cost:
            return 1
        link = building.get_current_upgrade_link(self.planet.page['resource'].content)
        if link:
            self.planet.resource['metal'].actual -= building.metal_cost
            self.planet.resource['crystal'].actual -= building.crystal_cost
            self.planet.resource['deuterium'].actual -= building.deuterium_cost
            self.planet.session.get(link)
            return 0
        return 2

    def run(self):
        while not self.stop:
            self.find_current_constructing_building_info()
            if len(self.buildings_queue) > 0:
                building = self.buildings_queue[0]
            else:
                time.sleep(5)
                continue

            state = self.upgrade_building(building)
            if state == 0:
                self.current_remaining_time = building.building_time
                self.building()
                self.buildings_queue.pop(0)
            elif state == 1:
                print('Waiting for enough materials!')
                time.sleep(self.calc_time_till_upgrade_is_possible(building) + 3)
            else:
                print('Could not acquire upgrade link, waiting and retrying...')

    def building(self):
        while self.current_remaining_time > 0:
            self.current_remaining_time -= 1
            time.sleep(1)

    def calc_time_till_upgrade_is_possible(self, building):
        return 5

    def find_current_constructing_building_info(self):
        """
        Refreshes the resource page, updates the building list if necessary.
        """

        def add_at_start_of_queue(numbers):
            supply = 'supply' + str(numbers[0])
            building = None
            for b in self.planet.building.keys():
                if self.planet.building[b].supply == supply:
                    building = self.planet.building[b]
            self.buildings_queue.insert(0, self.add_to_queue(building))
            self.current_remaining_time = numbers[1]
            self.building()
            self.buildings_queue.pop(0)

        self.planet.page['resource'].refresh_content()
        extract_resource_numbers = re.findall(FIND_ACTUAL_BUILDING_TIME, self.planet.page['resource'].content)

        numbers = []
        for number in extract_resource_numbers:
            [numbers.append(int(num)) for num in re.findall('[0-9\.]+', number)]

        if numbers:
            supply = 'supply' + str(numbers[0])
            if len(self.buildings_queue) == 0:
                add_at_start_of_queue(numbers)
            elif self.buildings_queue[0].building.supply != supply:
                add_at_start_of_queue(numbers)

    def currently_queued_buildings_with_name(self, name):
        count = 0
        for b in self.buildings_queue:
            if b.name == name:
                count += 1
        return count
