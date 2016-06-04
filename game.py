import re

import requests

from constants import *
from planet import Planet


class Game(object):
    UNIVERSE_SPEED = 1

    def __init__(self, server, user, password):
        self.server = server
        self.user = user
        self.password = password
        self.session = requests.Session()
        self.planets = {}
        self.current_planet = ''
        self.login()
        self.get_planets()
        self.current_planet = self.planets['main']
        Game.UNIVERSE_SPEED = self.get_universe_speed()

    def login(self):
        url = LOGIN_PAGE
        user = self.user
        password = self.password
        uni = self.server

        self.session.get(url)
        login_data = {'kid': '',
                      'uni': uni,
                      'login': user,
                      'pass': password}

        self.session.post(url, data=login_data, headers=HEADERS_DICT)

    def get_planets(self):
        self.planets = {'main': Planet(self.session)}

    def exit_game(self):
        self.session.close()

    def get_universe_speed(self):
        extract_resource_numbers = re.findall(FIND_UNIVERSE_SPEED, self.current_planet.page['resource'].content)
        numbers = []
        for number in extract_resource_numbers:
            numbers.append(re.findall('[0-9\.]+', number))
        return int(numbers[0][0])
