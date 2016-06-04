import sys

from gui.pyside.helper import *
import game
from constants import *
import os

import shutil

import requests

class MainFrame:
    def __init__(self, server=SERVER, user=USER, password=PASSWORD):
        app = QtGui.QApplication(sys.argv)
        self.window = load_ui_widget('main_frame.ui')
        self.game = game.Game(server, user, password)
        self.load_images()
        self.load_buttons()
        self.window.show()
        sys.exit(app.exec_())

    def refresh_current_planet_images(self):
        os.makedirs('resources/downloaded/', exist_ok=True)
        url = self.game.current_planet.resource_page_image_url
        response = requests.get(url, stream=True)
        with open('resources/downloaded/planet_buildings_resources.jpg', 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response

        url = self.game.current_planet.station_page_image_url
        response = requests.get(url, stream=True)
        with open('resources/downloaded/planet_buildings_station.jpg', 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response
        load_image(label=self.window.planetViewRessources, image='resources/downloaded/planet_buildings_resources.jpg')
        load_image(label=self.window.planetViewStation, image='resources/downloaded/planet_buildings_station.jpg')

    def load_images(self):
        self.refresh_current_planet_images()
        load_image(label=self.window.metal_mine, image='resources/metal_mine.png')
        load_image(label=self.window.crystal_mine, image='resources/crystal_mine.png')
        load_image(label=self.window.deuterium_mine, image='resources/deuterium_mine.png')
        load_image(label=self.window.solar_plant, image='resources/solar_plant.png')
        load_image(label=self.window.fusion_plant, image='resources/fusion_plant.png')
        load_image(label=self.window.solar_satellite, image='resources/solar_satellite.png')
        load_image(label=self.window.metal_storage, image='resources/metal_storage.png')
        load_image(label=self.window.crystal_storage, image='resources/crystal_storage.png')
        load_image(label=self.window.deuterium_storage, image='resources/deuterium_storage.png')
        load_image(label=self.window.robotics, image='resources/robotics.jpg')
        load_image(label=self.window.shipyard, image='resources/shipyard.jpg')
        load_image(label=self.window.research_lab, image='resources/research_lab.jpg')
        load_image(label=self.window.rocket_storage, image='resources/rocket_storage.jpg')
        load_image(label=self.window.alliance_depot, image='resources/alliance_depot.jpg')
        load_image(label=self.window.nanite_factory, image='resources/nanite_factory.jpg')
        load_image(label=self.window.terra_former, image='resources/terra_former.jpg')

    def load_buttons(self):
        self.window.b_metal_mine.clicked.connect(self.add_metal_mine_to_queue)

    def add_metal_mine_to_queue(self):
        print('test')


if __name__ == '__main__':
    MainFrame()
