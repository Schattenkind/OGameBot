import time

from constants import *
from info.page_info import Page
from info.resources import Resource, Energy
from buildings.building import Building
from buildings.queue import Queue
from threading import Thread


class Planet(object):
    """ Simulates a planet in ogame. Contains pages for the planet buildings and resources.
    """

    def __init__(self, session):
        """
        :param session: Current ogame session
        :param building_finished_callback: callable, executed when a building finishes
        :param building_started_callback: callable, executed when a new building starts
        """
        self.session = session

        # load pages
        self.page = {'resource': Page(self.session, RESOURCE_PAGE),
                     'overview': Page(self.session, OVERVIEW_PAGE)}

        self.resource = {'metal': Resource('Metal', self.page['resource']),
                         'crystal': Resource('Crystal', self.page['resource']),
                         'deuterium': Resource('Deuterium', self.page['resource']),
                         'energy': Energy('Energy', self.page['resource'])}

        self.building = {'metal_mine': Building('Metal Mine', Page(self.session, METAL_MINE), 'supply1'),
                         'crystal_mine': Building('Crystal Mine', Page(self.session, CRYSTAL_MINE), 'supply2'),
                         'deuterium_mine': Building('Deuterium Mine', Page(self.session, DEUTERIUM_MINE), 'supply3'),
                         'solar': Building('Solar', Page(self.session, SOLAR), 'supply4', energy_producer=True),
                         'fusion': Building('Fusion', Page(self.session, FUSION), 'supply12', energy_producer=True),
                         'metal_storage': Building('Metal Storage', Page(self.session, METAL_STORAGE), 'supply22'),
                         'crystal_storage': Building('Crystal Storage', Page(self.session, CRYSTAL_STORAGE),
                                                     'supply23'),
                         'deuterium_storage': Building('Deuterium Storage', Page(self.session, DEUTERIUM_STORAGE),
                                                       'supply24')
                         }

        self.buildings_queue = Queue(self)

        # add resource updater
        self.refresher = Thread(target=self.update_resources)
        self.refresher.daemon = True
        self.refresher.start()

        # start queue thread
        self.buildings_queue.start()

    def refresh_info(self):
        for page in self.page.keys():
            self.page[page].refresh_content()
        for resource in self.resource.keys():
            # not necessary to refresh the page since it was just refreshed
            self.resource[resource].refresh_info(refresh_page=False)
        for building in self.building.keys():
            self.building[building].refresh_info()

    def update_resources(self):
        while True:
            for resource in self.resource.keys():
                if resource != 'energy' and self.resource[resource].capacity > self.resource[resource].actual:
                    self.resource[resource].actual += self.resource[resource].production
            time.sleep(1)

    def add_to_queue(self, building):
        """
        :param building: building to be upgraded
        """
        return self.buildings_queue.add_to_queue(building)
