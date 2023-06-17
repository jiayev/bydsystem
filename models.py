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



class ChargingCar:
    SERVICE_FEE = 0.8
    def __init__(self, car_id, charging_volume, charging_mode, is_charging=False):
        self.car_id = car_id
        # 车辆的待充电量
        self.charging_volume = charging_volume
        # 添加一个属性来存储车辆的已充电量
        self.charged_volume = 0
        #充电模式
        self.charging_mode = charging_mode
        self.is_charging = is_charging
        self.bill = []
        # 假设快充模式每小时充电30度电，慢充模式每小时充电7度电
        if self.charging_mode == 'F':
            self.charge_rate = 30  # 度电/小时
        elif self.charging_mode == 'T':
            self.charge_rate = 7  # 度电/小时
    def start_charging(self):
        self.is_charging = True

    def stop_charging(self):
        self.is_charging = False

    def modify_remaining_volume(self, volume):
        self.charging_volume = volume

    def charge(self, time_unit):
        # 计算这个时间单位的充电量
        charge_this_unit = self.charge_rate * time_unit

        # 如果待充电量不足以供这个时间单位充电
        if self.charging_volume < charge_this_unit:
            # 将所有待充电量都转移到已充电量
            self.charged_volume += self.charging_volume
            self.charging_volume = 0
        else:
            # 否则，从待充电量中减去这个时间单位的充电量，并添加到已充电量
            self.charging_volume -= charge_this_unit
            self.charged_volume += charge_this_unit


    def is_charged(self):
        return self.charging_volume == 0

    def add_to_bill(self):
        # 在这里添加将费用添加到详单的逻辑
        pass

