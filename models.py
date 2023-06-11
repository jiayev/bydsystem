import datetime
import queue

class ChargingStation:
    def __init__(self, id, power, capacity):
        self.id = id
        self.power = power
        self.capacity = capacity
        self.queue = queue.Queue(maxsize=capacity)
        self.total_charging_time = 0

    def is_full(self):
        return self.queue.full()

    def add_car(self, charging_volume):
        self.queue.put(charging_volume)
        self.total_charging_time += charging_volume / self.power



