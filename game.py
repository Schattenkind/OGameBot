__author__ = 'Tobias'

import requests

from constants import *
from planet import Planet

class Game(object):
    def __init__(self, server, user, password):
        self.server = server
        self.user = user
        self.password = password
        self.session = requests.Session()
        self.planets = []
        self.current_planet = ''
        self.login()
        self.get_planets()
        self.current_planet = self.planets['main']

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
