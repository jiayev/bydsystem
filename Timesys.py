import time

from server import charging_cars


class TimeSystem:
    def __init__(self, start_time, time_unit, end_time,is_auto, step):
        #time_unit表示时间系统的每个周期的长度如秒，分
        self.end_time = end_time
        self.current_time = start_time
        self.start_time = start_time
        self.time_unit = time_unit
        self.is_auto = is_auto
        self.step = step

    def step_forward(self):
        while self.current_time <= self.end_time:
            self.check_and_operate()
            for car in charging_cars:
                car.charge(self.time_unit)
                car.calculate_fee()
                car.add_to_bill()
            self.current_time += self.step
            if not self.is_auto:
                break

    def auto_run(self):
        while self.current_time <= self.end_time:
            self.check_and_operate()
            for car in charging_cars:
                car.charge(self.time_unit)
                car.calculate_fee()
                car.add_to_bill()
            self.current_time += self.step
            time.sleep(self.time_unit)  # 假设time_unit以秒为单位

    def check_and_operate(self):
        # 在这里添加每个时间单位开始时进行的检查和操作
        pass

# 设定开始时间，结束时间，时间单位，是否自动运行，和step
start_time = 0
end_time = 24
# 时间系统从0小时开始，每个时间步为0.5小时，结束于24小时，自动运行
time_unit = 0.5
is_auto = True
step = 1

# 初始化时间系统
time_system = TimeSystem(start_time, time_unit, end_time, is_auto, step)

# 根据是否自动运行选择运行方式
if time_system.is_auto:
    time_system.auto_run()
else:
    time_system.step_forward()
