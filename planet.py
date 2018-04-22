import logging
from constants import *
from info.page_info import Page
from info.resources import Resource, Energy
from buildings.building import *
from buildings.queue import BuildQueue


logger = logging.getLogger('ogame_bot.planet')


class Planet(object):
    """ Simulates a planet in ogame. Contains pages for the planet buildings and resources.
    """

    def __init__(self, session, id='0'):
        """
        :param session: Current ogame session
        """
        self.session = session
        self.logger = logger
        self.buildings_queue = BuildQueue(self)

        # load pages
        self.page = {'resource': Page(self.session, RESOURCE_PAGE),
                     'overview': Page(self.session, OVERVIEW_PAGE),
                     'station': Page(self.session, STATION_PAGE)}

        self.resources = {'metal': Resource('Metal', self.page['resource']),
                          'crystal': Resource('Crystal', self.page['resource']),
                          'deuterium': Resource('Deuterium', self.page['resource']),
                          'energy': Energy('Energy', self.page['resource'])}

        self.buildings = {METAL_MINE: Building('Metal Mine', Page(self.session, METAL_MINE_URL), 'supply1'),
                          CRYSTAL_MINE: Building('Crystal Mine', Page(self.session, CRYSTAL_MINE_URL),
                                                 'supply2'),
                          DEUTERIUM_MINE: Building('Deuterium Mine', Page(self.session, DEUTERIUM_MINE_URL),
                                                   'supply3'),
                          SOLAR: Building('Solar', Page(self.session, SOLAR_URL), 'supply4',
                                          energy_producer=True),
                          FUSION: Building('Fusion', Page(self.session, FUSION_URL), 'supply12',
                                           energy_producer=True),
                          METAL_STORAGE: Building('Metal Storage', Page(self.session, METAL_STORAGE_URL),
                                                  'supply22'),
                          CRYSTAL_STORAGE: Building('Crystal Storage', Page(self.session, CRYSTAL_STORAGE_URL),
                                                    'supply23'),
                          DEUTERIUM_STORAGE: Building('Deuterium Storage',
                                                      Page(self.session, DEUTERIUM_STORAGE_URL),
                                                      'supply24')
                          }

        self.id = id
        self.fill_queue()
        self.logger.info('Starting queue for planet ' + self.id)
        self.buildings_queue.start()

    def refresh_info(self):
        self.logger.debug("Start refresh of planet info. (Planet ID " + self.id + ")")
        for page in self.page.keys():
            self.page[page].refresh_content()
        for resource in self.resources.keys():
            # not necessary to refresh the page since it was just refreshed
            self.resources[resource].refresh_info(refresh_page=False)
        for building in self.buildings.keys():
            self.buildings[building].refresh_info()

    def fill_queue(self):
        self.refresh_info()
        metal_mine_level = self.buildings[METAL_MINE].level
        crystal_mine_level = self.buildings[CRYSTAL_MINE].level
        deuterium_mine_level = self.buildings[DEUTERIUM_MINE].level
        solar_level = self.buildings[SOLAR].level

        current_energy = self.resources['energy'].actual

        message = "Figuring out what to do next... Current planet (ID: " + self.id + ") state:\n"
        for b in self.buildings:
            message += str(self.buildings[b]) + "\n"

        for r in self.resources:
            message += str(self.resources[r]) + "\n"

        self.logger.info(message)

        if current_energy < 0 and solar_level < 15:
            self.upgrade_building(self.buildings[SOLAR])

        elif metal_mine_level - 3 < crystal_mine_level:
            self.upgrade_building(self.buildings[METAL_MINE])

        elif crystal_mine_level - 3 > deuterium_mine_level and crystal_mine_level > 10:
            self.upgrade_building(self.buildings[DEUTERIUM_MINE])

        else:
            self.logger.info("Adding metal mine to the building queue. (Planet " + self.id + ")")
            self.upgrade_building(self.buildings[CRYSTAL_MINE])


    def upgrade_building(self, building):
        """
        :param building: building to be upgraded
        """
        return self.buildings_queue.add_to_queue(building)