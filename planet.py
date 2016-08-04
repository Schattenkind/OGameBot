from threading import Timer
import re

from constants import *
from info.page_info import Page
from info.resources import Resource, Energy
from buildings.building import Building
from build_queue.queue import Queue


def find_planet_image_for_page(page_content):
    print(page_content)
    image_url = re.findall(FIND_PLANET_IMAGE, page_content)
    print(image_url)
    return re.findall("https://.{0,300}\)", image_url[0])[0][:-1]

class Planet(object):
    """ Simulates a planet in ogame. Contains pages for the planet buildings and resources.
    """

    def __init__(self, session, id='0'):
        """
        :param session: Current ogame session
        :param building_finished_callback: callable, executed when a building finishes
        :param building_started_callback: callable, executed when a new building starts
        """
        self.session = session

        # load pages
        self.page = {'resource': Page(self.session, RESOURCE_PAGE),
                     'overview': Page(self.session, OVERVIEW_PAGE),
                     'station': Page(self.session, STATION_PAGE)}

        self.resource = {'metal': Resource('Metal', self.page['resource']),
                         'crystal': Resource('Crystal', self.page['resource']),
                         'deuterium': Resource('Deuterium', self.page['resource']),
                         'energy': Energy('Energy', self.page['resource'])}

        self.building = {'metal_mine': Building('Producers', 'Metal Mine', Page(self.session, METAL_MINE), 'supply1'),
                         'crystal_mine': Building('Producers', 'Crystal Mine', Page(self.session, CRYSTAL_MINE),
                                                  'supply2'),
                         'deuterium_mine': Building('Producers', 'Deuterium Mine', Page(self.session, DEUTERIUM_MINE),
                                                    'supply3'),
                         'solar': Building('Producers', 'Solar', Page(self.session, SOLAR), 'supply4',
                                           energy_producer=True),
                         'fusion': Building('Producers', 'Fusion', Page(self.session, FUSION), 'supply12',
                                            energy_producer=True),
                         'metal_storage': Building('Storage', 'Metal Storage', Page(self.session, METAL_STORAGE),
                                                   'supply22'),
                         'crystal_storage': Building('Storage', 'Crystal Storage', Page(self.session, CRYSTAL_STORAGE),
                                                     'supply23'),
                         'deuterium_storage': Building('Storage', 'Deuterium Storage',
                                                       Page(self.session, DEUTERIUM_STORAGE),
                                                       'supply24')
                         }

        self.buildings_queue = Queue(self)
        self.id = id

        # add resource updater
        self.update_resources_periodic()

        # start build_queue thread
        self.buildings_queue.start()

    @property
    def resource_page_image_url(self):
        return find_planet_image_for_page(self.page['resource'].content)

    @property
    def station_page_image_url(self):
        return find_planet_image_for_page(self.page['station'].content)

    def refresh_info(self):
        for page in self.page.keys():
            self.page[page].refresh_content()
        for resource in self.resource.keys():
            # not necessary to refresh the page since it was just refreshed
            self.resource[resource].refresh_info(refresh_page=False)
        for building in self.building.keys():
            self.building[building].refresh_info()

    def update_resources_periodic(self):
        for resource in self.resource.keys():
            if resource != 'energy' and self.resource[resource].capacity > self.resource[resource].actual:
                self.resource[resource].actual += self.resource[resource].production
        t = Timer(1, self.update_resources_periodic)
        t.setDaemon(True)
        t.start()

    def add_to_queue(self, building):
        """
        :param building: building to be upgraded
        """
        return self.buildings_queue.add_to_queue(building)

