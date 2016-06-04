import tkinter as tk
import time
from constants import *
from threading import Thread
from gui.helper import convert_to_readable_time_string

import pygubu

from game import Game


class Application:
    def __init__(self, master, server, user, password):
        self.__amount_of_buildings = 0
        self.__queue_position = 1
        self.master = master

        # start the actual bot
        self.game = Game(server, user, password)

        # 1: Create a builder
        self.builder = builder = pygubu.Builder()

        # 2: Load an ui file
        builder.add_from_file('main_frame.ui')

        # 3: Create the widget using a master as parent
        self.mainwindow = builder.get_object('MainFrame', master)
        self.metal = builder.get_object('metal', master)
        self.crystal = builder.get_object('crystal', master)
        self.deuterium = builder.get_object('deuterium', master)
        self.energy = builder.get_object('energy', master)
        self.buildings_tree = builder.get_object('buildings', master)
        self.buildings_queue_tree = builder.get_object('queue', master)

        # buttons
        self.add_to_queue_button = builder.get_object('add_to_queue', master)
        self.add_to_queue_button['command'] = self.add_to_queue

        master.wm_title('OGameBot - ' + USER)

        # start gui and game updater
        self.update_gui()
        self.update_periodic()
        self.refresher = Thread(target=self.auto_refresh_info)
        self.refresher.daemon = True
        self.refresher.start()

    def update_gui(self):
        def empty_building_list():
            for item in self.buildings_tree.get_children():
                self.buildings_tree.delete(item)

        def add_building(building, category=''):
            values = [str(building.level), convert_to_readable_time_string(building.building_time),
                      str(building.metal_cost),
                      str(building.crystal_cost), str(building.deuterium_cost), str(building.energy)]
            self.buildings_tree.insert(category, self.__amount_of_buildings, building.name, text=building.name,
                                       values=values)
            self.__amount_of_buildings += 1

        self.__amount_of_buildings = 0
        empty_building_list()
        for b in sorted(self.game.current_planet.building.items(), key=lambda x: int(x[1].supply[6:])):
            add_building(b[1])

    def refresh_info_from_web(self):
        self.game.current_planet.refresh_info()
        self.update_gui()

    def auto_refresh_info(self):
        while True:
            self.refresh_info_from_web()
            time.sleep(60)

    def update_periodic(self):
        def update_resources():
            self.metal['text'] = str(int(self.game.current_planet.resource['metal'].actual))
            self.crystal['text'] = str(int(self.game.current_planet.resource['crystal'].actual))
            self.deuterium['text'] = str(int(self.game.current_planet.resource['deuterium'].actual))
            self.energy['text'] = str(self.game.current_planet.resource['energy'].actual)

        def update_queue():
            items = self.buildings_queue_tree.get_children()
            if len(items) > 0 and len(self.game.current_planet.buildings_queue.buildings_queue) > 0:
                first_item_name = self.buildings_queue_tree.item(items[0], 'text')
                next_building = self.game.current_planet.buildings_queue.buildings_queue[0]
                if first_item_name != next_building.name:
                    self.buildings_queue_tree.insert('', 0, next_building.name + '0815',
                                                     text=next_building.name,
                                                     values=[str(next_building.level),
                                                             convert_to_readable_time_string(
                                                                 next_building.building_time)])
                i = self.game.current_planet.buildings_queue.current_remaining_time
                self.buildings_queue_tree.set(items[0], column=1, value=convert_to_readable_time_string(i))
            elif len(self.game.current_planet.buildings_queue.buildings_queue) > 0:
                next_building = self.game.current_planet.buildings_queue.buildings_queue[0]
                self.buildings_queue_tree.insert('', 0, next_building.name + '0815', text=next_building.name,
                                                 values=[str(next_building.level),
                                                         convert_to_readable_time_string(next_building.building_time)])
            else:
                for item in self.buildings_queue_tree.get_children():
                    self.buildings_queue_tree.delete(item)
            return

        update_resources()
        update_queue()
        self.master.after(1000, self.update_periodic)

    def add_to_queue(self):
        item = self.buildings_tree.selection()
        building = ''
        for b in self.game.current_planet.building.keys():
            if self.game.current_planet.building[b].name == item[0]:
                building = self.game.current_planet.building[b]
        if building:
            queue_item = self.game.current_planet.add_to_queue(building)
            self.buildings_queue_tree.insert('', self.__queue_position, queue_item.name + str(self.__queue_position),
                                             text=queue_item.name,
                                             values=[str(queue_item.level),
                                                     convert_to_readable_time_string(queue_item.building_time)])
            self.__queue_position += 1


if __name__ == '__main__':
    root = tk.Tk()
    app = Application(root, SERVER, USER, PASSWORD)
    root.mainloop()
