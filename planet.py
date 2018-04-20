from threading import Timer
import re

from constants import *
from info.page_info import Page
from info.resources import Resource, Energy
from buildings.building import *


class Planet(object):
    """ Simulates a planet in ogame. Contains pages for the planet buildings and resources.
    """

    def __init__(self, session, id='0'):
        """
        :param session: Current ogame session
        """
        self.session = session

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

    def refresh_info(self):
        for page in self.page.keys():
            self.page[page].refresh_content()
        for resource in self.resources.keys():
            # not necessary to refresh the page since it was just refreshed
            self.resources[resource].refresh_info(refresh_page=False)
        for building in self.buildings.keys():
            self.buildings[building].refresh_info()

    def upgrade_building(self, building):
        """
        :param building: building to be upgraded
        """
        self.page['resource'].refresh_content()
        if self.resources['metal'].actual < building.metal_cost:
            return 1
        if self.resources['crystal'].actual < building.crystal_cost:
            return 1
        if self.resources['deuterium'].actual < building.deuterium_cost:
            return 1
        link = building.get_current_upgrade_link(self.page['resource'].content)
        return self.session.get(link)
