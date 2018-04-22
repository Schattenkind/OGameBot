import re
import requests
import logging
import os
import time

from info.page_info import Page
from constants import *


logger = logging.getLogger('ogame_bot')


def initialize_logger():
    # create logger
    logger.setLevel(logging.DEBUG)

    # create file handler which logs even debug messages
    number_of_sessions = 0
    file_name = "session_0.log"
    while os.path.isfile(file_name):
        file_name = "session_" + str(number_of_sessions) + ".log"
        number_of_sessions += 1
    fh = logging.FileHandler(file_name)
    fh.setLevel(logging.DEBUG)

    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)


class Game(object):
    UNIVERSE_SPEED = 1
    UNIVERSE_SPEED_FLEET = 1

    def __init__(self, server, user, password):
        self.logger = logger

        self.server = server
        self.user = user
        self.password = password
        self.session = requests.Session()

        self.planets = {}
        self.login()

        Game.UNIVERSE_SPEED = self.get_basic_parameter_value(FIND_UNIVERSE_SPEED)
        if Game.UNIVERSE_SPEED == 0:
            self.logger.warning("Could not set universe speed! Setting it to 1")
            Game.UNIVERSE_SPEED = 1
        else:
            self.logger.info("Universe speed has been set to: " + str(Game.UNIVERSE_SPEED))

        Game.UNIVERSE_SPEED_FLEET = self.get_basic_parameter_value(FIND_UNIVERSE_SPEED_FLEET)
        if Game.UNIVERSE_SPEED_FLEET == 0:
            self.logger.warning("Could not set universe fleet speed! Setting it to 1")
            Game.UNIVERSE_SPEED_FLEET = 1
        else:
            self.logger.info("Universe fleet speed has been set to: " + str(Game.UNIVERSE_SPEED_FLEET))
        self.get_planets()

        self.current_planet = self.planets['main']

    def login(self):
        url = LOGIN_PAGE
        user = self.user
        password = self.password
        uni = self.server

        self.logger.info("Trying to login as user " + self.user)
        self.session.get(url)
        self.logger.debug("Get with URL: " + url)
        login_data = {'kid': '',
                      'uni': uni,
                      'login': user,
                      'pass': password}

        self.session.post(url, data=login_data, headers=HEADERS_DICT)
        self.logger.debug("Post with URL: " + url + "; data: " + str(login_data) + "; headers: "+ str(HEADERS_DICT))

    def get_planets(self):
        from planet import Planet
        self.planets = {'main': Planet(self.session)}

    def exit_game(self):
        self.logger.info("Exiting the game and closing the session.")
        self.session.close()

    def get_basic_parameter_value(self, value):
        extract_resource_numbers = re.findall(value, Page(self.session, RESOURCE_PAGE).content)
        numbers = []
        for number in extract_resource_numbers:
            numbers.append(re.findall('[0-9.]+', number))
        try:
            number = int(numbers[0][0])
            self.logger.debug("Found number " + str(number) + " with regex: " + value)
        except IndexError:
            self.logger.warning("Couldn't find any number with regex: " + value)
            number = 0
        return number


if __name__ == "__main__":
    initialize_logger()
    try:
        Game(SERVER, USER, PASSWORD)
        while True:
            time.sleep(1)
    except Exception as e:
        logger.exception("Uncaught Exception was raised! Exiting")
