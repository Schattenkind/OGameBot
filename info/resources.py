import re
import logging

from constants import FIND_RESOURCE_ACT_CAP_PROD, FIND_ENERGY


__all__ = ['Resource', 'Energy', 'METAL', 'CRYSTAL', 'DEUTERIUM', 'ENERGY']

logger = logging.getLogger('ogame_bot.info.resources')


METAL = 0
CRYSTAL = 1
DEUTERIUM = 2
ENERGY = 3


class Resource(object):
    def __init__(self, name, info_page):
        self.logger = logger
        self.name = name
        self.actual = 0
        self.production = 0
        self.capacity = 0
        self._info_page = info_page
        self.refresh_info()

    def __str__(self):
        return "Resource {name}(actual: {actual}; production: {production}; capacity: {capacity})".format(
            name=self.name, actual=self.actual, production=self.production, capacity=self.capacity)

    def extract_resource_info(self):
        extract_resource_numbers = re.findall(FIND_RESOURCE_ACT_CAP_PROD.format(name=self.name.lower()),
                                              self._info_page.content)
        numbers = []
        for number in extract_resource_numbers:
            numbers.append(re.findall('[0-9\.]+', number))
        if not numbers:
            return 0, 0, 0
        return numbers[0]

    def refresh_info(self, refresh_page=True):
        if refresh_page:
            self._info_page.refresh_content()
        numbers = self.extract_resource_info()
        self.actual = int(numbers[1])
        self.capacity = int(numbers[2])
        self.production = float(numbers[3])


class Energy(Resource):
    def extract_resource_info(self):
        extract_resource_numbers = re.findall(FIND_ENERGY, self._info_page.content)
        numbers = []
        for number in extract_resource_numbers:
            n = re.findall('.[0-9\.]+', number)[1]
            try:
                numbers.append(int(n))
            except ValueError:
                numbers.append(int(n[1:]))
        return numbers[0]

    def refresh_info(self, refresh_page=True):
        if refresh_page:
            self._info_page.refresh_content()
        number = self.extract_resource_info()
        self.actual = int(number)
        self.capacity = int(number)
        self.production = int(number)
