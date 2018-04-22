from constants import *

import re
import time
import datetime
import threading
import logging

logger = logging.getLogger('ogame_bot.buildings.queue')


class BuildQueue(threading.Thread):
    def __init__(self, planet):
        threading.Thread.__init__(self, daemon=True)
        self.logger = logger
        self.planet = planet
        self.buildings_queue = []
        self.current_remaining_time = 0
        self.stop = False

    def add_to_queue(self, building):
        self.logger.info("Adding " + building.name + " to the building queue. (Planet ID " + self.planet.id + ")")
        self.buildings_queue.append(building)
        return True

    def upgrade_building(self, building):
        """
        :param building : queue item to upgrade
        :return: 0 - building is successfully upgrading
                 1 - not enough materials
                 2 - other reason why it could not be upgraded (e.g. other building still being build)
        """
        self.planet.refresh_info()
        if self.planet.resources['metal'].actual < building.metal_cost:
            self.logger.info("Not enough metal to upgrade! Waiting.. (Planet ID " + self.planet.id + ")")
            return 1
        if self.planet.resources['crystal'].actual < building.crystal_cost:
            self.logger.info("Not enough crystal to upgrade! Waiting.. (Planet ID " + self.planet.id + ")")
            return 1
        if self.planet.resources['deuterium'].actual < building.deuterium_cost:
            self.logger.info("Not enough deuterium to upgrade! Waiting.. (Planet ID " + self.planet.id + ")")
            return 1
        link = building.get_current_upgrade_link(self.planet.page['resource'].content)
        if link:
            self.planet.resources['metal'].actual -= building.metal_cost
            self.planet.resources['crystal'].actual -= building.crystal_cost
            self.planet.resources['deuterium'].actual -= building.deuterium_cost
            self.logger.info("Starting upgrade of " + building.name + " with link " + link + " (Planet ID " + self.planet.id + ")")
            self.planet.session.get(link)
            self.logger.info("Required time: " + str(datetime.timedelta(seconds=building.building_time)))
            return 0
        return 2

    def run(self):
        while not self.stop:
            self.find_current_constructing_building_info()
            if len(self.buildings_queue) > 0:
                building = self.buildings_queue[0]
            else:
                self.logger.debug("Queue is empty trying to fill it... (Planet " + self.planet.id + ")")
                self.planet.fill_queue()
                continue

            state = self.upgrade_building(building)
            if state == 0:
                self.current_remaining_time = building.building_time
                self.building()
                self.buildings_queue.pop(0)
            elif state == 1:
                self.logger.info("Waiting for enough materials! (Planet " + self.planet.id + ")")
                time.sleep(self.calc_time_till_upgrade_is_possible(building) + 3)
            else:
                self.logger.warning(
                    "Could not acquire upgrade link, waiting and retrying...(Planet " + self.planet.id + ")")
                time.sleep(3)

    def building(self):
        time.sleep(self.current_remaining_time + 1)

    def calc_time_till_upgrade_is_possible(self, building):
        return 5

    def find_current_constructing_building_info(self):
        """
        # TODO this is used to find buildings which are already building but is buggy
        Refreshes the resource page, updates the building list if necessary.
        """
        return

        def add_at_start_of_queue(numbers):
            supply = 'supply' + str(numbers[0])
            building = None
            for b in self.planet.buildings.keys():
                if self.planet.buildings[b].supply == supply:
                    building = self.planet.buildings[b]
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
