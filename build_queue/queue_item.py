import threading

TYPE_BUILDING = 0
TYPE_RESEARCH = 1
TYPE_SHIPYARD = 2
TYPE_OTHER = 3

class Item(object):
    def __init__(self, action, duration=0, item_type=TYPE_BUILDING):
        self.item_type = item_type
        self.action = action
        self.remaining_duration = duration

    def _start_timer(self):
        self.remaining_duration -= 1
        t = threading.Timer(1, self._start_timer())

    def activate(self):
        self.action()
