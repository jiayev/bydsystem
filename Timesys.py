import time
import sqlite3

from server import charging_cars, add_charging_car,wait_list


class TimeSystem:
    def __init__(self, start_time, time_unit, end_time,is_auto, step,wait_list):
        #time_unit表示时间系统的每个周期的长度如秒，分
        self.end_time = end_time
        self.current_time = start_time
        self.start_time = start_time
        self.time_unit = time_unit
        self.is_auto = is_auto
        self.step = step

        self.wait_list = wait_list

    def update_charging_station(self, station_id, status, current_charging_car, current_waiting_car, on_service):
        # 连接到SQLite数据库
        conn = sqlite3.connect('charging_stations.db')

        # 创建一个Cursor对象
        c = conn.cursor()

        # 执行UPDATE语句
        c.execute("""
        UPDATE charging_stations
        SET status = ?, current_charging_car = ?, current_waiting_car = ?, on_service = ?
        WHERE station_id = ?
        """, (status, current_charging_car, current_waiting_car, on_service, station_id))

        # 提交事务
        conn.commit()

        # 关闭连接
        conn.close()
    def step_forward(self):
        while self.current_time <= self.end_time:
            self.check_and_operate()
            for car in charging_cars.items():
                car.charge(self.time_unit)
                car.calculate_fee()
                car.add_to_bill()
            self.current_time += self.step
            if not self.is_auto:
                break

    def auto_run(self):
        while self.current_time <= self.end_time:
            for _ in range(int(1 / self.time_unit)):  # 这个循环会使得check_and_operate每秒运行一次
                self.check_and_operate()
                time.sleep(1)  # 暂停一秒
            for station_id, car in list(charging_cars.items()):  # 遍历复制的字典，以防在迭代过程中改变字典
                car.charge(self.time_unit)
                car.calculate_fee()
                car.add_to_bill()
                if car.is_charged():  # 如果车辆已经充电完成
                    del charging_cars[station_id]  # 从正在充电的车辆字典中移除
                    self.update_charging_station(car.station_id, 'free', None, None, 1)  # 将充电站状态更新为'free'
                    # 这里可以添加更多的清理工作，如更新数据库等
            self.current_time += self.step
            time.sleep(self.time_unit)  # 假设time_unit以秒为单位

    def check_and_operate(self):
        # 在这里添加每个时间单位开始时进行的检查和操作

        add_charging_car(self.wait_list)#把等待列表里的车添加到正在充电列表
        pass

# 设定开始时间，结束时间，时间单位，是否自动运行，和step
start_time = 0
end_time = 24
# 时间系统从0小时开始，每个时间步为0.5小时，结束于24小时，自动运行
time_unit = 0.5
is_auto = True
step = 1

# 初始化时间系统
time_system = TimeSystem(start_time, time_unit, end_time, is_auto, step, wait_list)


# 根据是否自动运行选择运行方式
if time_system.is_auto:
    time_system.auto_run()
else:
    time_system.step_forward()
