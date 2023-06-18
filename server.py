import time
import traceback
import sqlite3
import waitinglist
from waitinglist import WaitingList
from waitinglist import WaitingNode
from waitinglist import EventList
from waitinglist import EventNode
from sqlite3 import Error
from flask import Flask, request, jsonify
import threading
from models import datetime, ChargingCar
import queue
import op_sql

app = Flask(__name__)
wait_list = WaitingList()
#时间
# 全局的充电车辆列表
charging_cars = {"A": [], "B": [], "C": [], "D": [], "E": []}
# 设定开始时间，结束时间，时间单位，是否自动运行，和step
start_time = 0
end_time = 24
# 时间系统从0小时开始，每个时间步为0.5小时，结束于24小时，自动运行
time_unit = 0.5
is_auto = False
step = 1

charging_requests = {}
#创建一个存储current_car中的
cars = {}

event_list = EventList()


# 创建两个队列，一个用于快充的请求，另一个用于慢充的请求
# fast_charging_queue = queue.Queue(maxsize=6)
# slow_charging_queue = queue.Queue(maxsize=6)

def isWaitingCar(car_id):
    if cars[car_id] == None:
        return False
    else:
        return True

# 创建一个 Event 对象
stop_charging_cars = threading.Event()




# def display_charging_cars():
#     while not stop_charging_cars.is_set():
#         for id, car in charging_cars.items():
#             print(f"Car ID: {id}")
#             print(f"Required charge: {charging_requests[id]['charging_volume']}")
#             print(f"Charged so far: {car['charged_volume']}")
#             print(f"Charging mode: {charging_requests[id]['charging_mode']}")
#             print()
#         time.sleep(5)  # 每5秒打印一次

def create_account_table():
    conn = sqlite3.connect('accounts.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE accounts
                 (username text, password text, isadmin boolean)''')

    conn.commit()
    conn.close()

# 显示时间系统的当前时间
@app.route('/time_system/current_time', methods=['GET'])
def get_current_time():
    return time_system.current_time, 200


def setup():
    op_sql.turn_on_all_charging_station()
    print("All charging stations are on.\n")

@app.route('/')
def index():
    print("Client connected.\n")
    return "Client connected.", 200

@app.route('/register', methods=['POST'])
def register_account():
    username = request.form.get('username')  # 使用request.form获取POST数据
    password = request.form.get('password')
    isadmin = request.form.get('isadmin')
    conn = sqlite3.connect('accounts.db')
    # 如果数据库中不存在accounts表，则创建accounts表
    if conn.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='accounts'").fetchone()[0] == 0:
        create_account_table()
        print("accounts table created\n")
    c = conn.cursor()

    c.execute("INSERT INTO accounts VALUES (?,?,?)", (username, password,isadmin))

    conn.commit()
    conn.close()
    return "Registration successful.", 200  # 确保注册成功后，返回200状态码

def check_account(username, password):
    conn = sqlite3.connect('accounts.db')
    c = conn.cursor()
    c.execute("SELECT * FROM accounts WHERE username=? AND password=?", (username, password))
    # 根据得到的查询结果，判断是否为管理员账户
    result = c.fetchone()
    conn.close()
    # 打印查询结果
    print(result)

    if result is None:
        return 0
    else:
        if result[2] == 'y':
            return 2
        return 1

@app.route('/apply_event', methods=['POST'])
# class EventNode:
#     def __init__(self, event_type, event_time, car_id, charge_value, charge_mode):
#         self.event_type = event_type
#         self.event_time = event_time
#         self.car_id = car_id
#         self.charge_value = charge_value
#         self.charge_mode = charge_mode
#         self.next = None
def apply_event():
    event_type = request.form.get('event_type')
    event_time = request.form.get('event_time')
    car_id = request.form.get('car_id')
    charge_value = request.form.get('charge_value')
    charge_mode = request.form.get('charge_mode')
    event_list.add(event_type, event_time, car_id, charge_value, charge_mode)
    return "Event applied.", 200


@app.route('/login', methods=['POST'])

def login():
    isadmin = False
    username = request.form.get('username')  # 从请求中获取用户名
    password = request.form.get('password')  # 从请求中获取密码
    # 调用check_account函数，检查用户名和密码是否正确
    result = check_account(username, password)
    if result == 2:
        print("Login as ",username," an administrator.")
        return "Login successful. You are an administrator.", 201  # 返回登录成功消息和 201 状态码
    elif result == 1:
        print("Login as ",username," a user.")
        return "Login successful.", 200  # 返回登录成功消息和 200 状态码
    else:  # 如果 check_account 函数返回 False
        return "Invalid username or password.", 401  # 返回错误消息和 401 状态码


@app.route('/event_request', methods=['POST'])
def event_request(event_type = None, id = None, value = None, charge_type = None):
    # 如果参数为空，则从请求中获取参数
    if event_type is None:
        event_type = request.form.get('event_type')
        id = request.form.get('id')
        value = request.form.get('value')
        charge_type = request.form.get('charge_type')
    # 如果event_type不为ABC，charge_type不为F/T/O，则返回错误信息
    elif event_type not in ['A', 'B', 'C'] or charge_type not in ['F', 'T', 'O']:
        return "Invalid event type or charge type.", 400
    if event_type == 'A':
        WaitingList.add(wait_list,id,value,charge_type)
    elif event_type == 'B':
            if op_sql.is_on_station(id) == value:
                return "Charging station is already on/off.", 400
            op_sql.turn_on_off_charging_station(id,value)
            if value == 1:
                return "Charging station is on.", 200
            else:
                return "Charging station is off.", 200
    elif event_type == 'C':
        if wait_list.isExist(id) == False:
            station_id = op_sql.query_station_by_car(id)
            if station_id is not None:
                if charge_type != 'O' and charge_type != wait_list.getInfo(id, 'charge_type'):
                    if value == -1:
                        WaitingList.add(wait_list,id,wait_list.getInfo(id, 'charge_value'),charge_type)
                    else:
                        WaitingList.add(wait_list,id,value,charge_type)
                    if charging_cars[station_id] is not None:
                        charging_cars[station_id].remove(id)
                    else:
                        # 根据id移除cars中的车辆
                        cars[id] = None
                    return "Event request successful.", 200
                else:
                    if charging_cars[station_id] is not None:
                        charging_cars[station_id].modify_remaining_volume(value)
                    else:
                        cars[id].modify_remaining_volume(value)

                    
            
        elif value == 0:
            WaitingList.remove(wait_list,id)
        elif charge_type != 'O':
            WaitingList.changeInfo(wait_list,id,value,charge_type)
        else:
            WaitingList.changeInfo(wait_list,id,value,wait_list.getInfo(id, 'charge_type'))

    return "Event request successful.", 200  # 返回登录成功消息和 200 状态码


@app.route('/charging_request', methods=['POST'])
# 需要重写
# 已经改为这个函数只负责接收请求，然后调用event_request函数
def charging_request():
    request_data = request.get_json()
    vehicle_id = request_data['vehicle_id']
    charging_mode = request_data['charging_mode']
    charging_volume = request_data['charging_volume']

    try:
        response = event_request('A', vehicle_id, charging_volume, charging_mode)

        return response

    except Exception as e:

        print("Error occurred:", e)

        print("Full traceback:")

        traceback.print_exc()

        return {"status": "fail", "message": "An error occurred while processing your request."}, 500
    
def add_charging_car(waiting_list):
    conn = sqlite3.connect('charging_stations.db')
    c = conn.cursor()

    c.execute('SELECT * FROM charging_stations')
    charging_stations = c.fetchall()

    for row in charging_stations:
        station_id = row[0]
        station_type = row[1]
        status = row[2]
        current_charging_car = row[3]
        charging_queue = row[4]
        current_waiting_car = row[5]
        on_service = row[6]

        if status == 'free' and on_service == 1:
            if current_charging_car is None and current_waiting_car is not None:
                # 将等待的车辆移动到正在充电的车辆
                current_charging_car = cars[current_waiting_car]  # 从字典中获取车辆对象
                del cars[current_waiting_car]  # 从字典中移除该车辆
                car_id, charge_value, charge_mode = current_charging_car.getInfo()
                new_car = ChargingCar(car_id, charge_value, charge_mode, is_charging=True)

                # 将车辆添加到充电站
                charging_cars[station_id].append(new_car)

                c.execute(f"UPDATE charging_stations SET status = 'busy', current_charging_car = ? WHERE station_id = ?", (current_charging_car.car_id, station_id))
                c.execute(f"UPDATE charging_stations SET current_waiting_car = ? WHERE station_id = ?", (None, station_id))
                conn.commit()

            elif current_charging_car is None:
                # 从等待队列中获取车辆并将其添加到正在充电的车辆
                if station_type == 'F':
                    car_node = waiting_list.getFirstFast()
                else:
                    car_node = waiting_list.getFirstSlow()

                if car_node is not None:
                    waiting_list.remove(car_node.car_id)
                    current_charging_car = car_node
                    car_id, charge_value, charge_mode = current_charging_car.getInfo()
                    new_car = ChargingCar(car_id, charge_value, charge_mode, is_charging=True)

                    # 将车辆添加到充电站
                    charging_cars[station_id].append(new_car)
                    c.execute(f"UPDATE charging_stations SET status = 'busy', current_charging_car = ? WHERE station_id = ?", (current_charging_car.car_id, station_id))
                    conn.commit()

            elif current_waiting_car is None:
                # 从等待队列中获取车辆并将其添加到等待的车辆
                if station_type == 'F':
                    car_node = waiting_list.getFirstFast()
                else:
                    car_node = waiting_list.getFirstSlow()

                if car_node is not None:
                    waiting_list.remove(car_node.car_id)
                    current_waiting_car = car_node

                    # 添加车辆到字典
                    cars[current_waiting_car.car_id] = current_waiting_car

                    c.execute(f"UPDATE charging_stations SET current_waiting_car = ? WHERE station_id = ?", (current_waiting_car.car_id, station_id))
                    conn.commit()

    conn.close()


def is_charging_station_free(charging_station):
    return op_sql.is_busy_station(charging_station)

# def push_list_to_charging_station(wait_list):
#     return 200




def get_charging_cars():
    # 返回一个列表，每个元素都是一个字符串，描述了一个正在充电的汽车的信息
    return [
        f'Car ID: {car_id}, Need charging volume: {info["need_charging_volume"]}, Charged volume: {info["charged_volume"]}, Charging mode: {info["charging_mode"]}'
        for car_id, info in charging_cars.items()
    ]
@app.route('/waiting_vehicles', methods=['GET'])
def waiting_vehicals():
    request_data = ""
    # 对g.wait_list中的每个WaitingNode元素使用函数WaitingNode.getInfo，返回self.car_id, self.charge_value, self.charge_mode，整合为一个字符串
    for i in range(wait_list.getLength()):
        request_data += WaitingNode.getInfo(wait_list[i])

    return {"message": request_data}, 200

def get_first_waiting_vehicle(charging_mode):
    # 返回等待队列中的第一个车辆
    if charging_mode == 'F':
        return wait_list.getFirstFast().car_id
    elif charging_mode == 'T':
        return wait_list.getFirstSlow().car_id

@app.route('/charging_detail', methods=['GET'])
def charging_detail():
    username = request.form['username']
    # 需要一些逻辑来生成和返回充电详单信息
    return {"message": "Charging detail returned successfully."}, 200

@app.route('/charging_stations', methods=['GET'])
# 已经重写
def assign_charging_station(car_id, charging_mode):
    free_station = op_sql.get_first_free_station(charging_mode)
    return free_station

@app.route('/get_bill', methods=['GET'])
def get_bill(car_id):
    # todo: 生成账单
    return {"message": "Bill returned successfully."}, 200

@app.route('/charging_stations_inf', methods=['GET'])
#返回所有充电桩状态信息
def get_charging_stations():
    # 连接到你的数据库
    conn = sqlite3.connect('charging_stations.db')

    # 创建一个Cursor对象
    c = conn.cursor()

    # 执行SQL查询来获取所有充电桩的状态
    c.execute('SELECT * FROM charging_stations')

    # 获取查询结果
    result = c.fetchall()

    # 关闭数据库连接
    conn.close()

    # 将查询结果转化为字符串，每次结果占一行
    result_str = '\n'.join([str(row) for row in result])


    # 返回查询结果
    return {"message": result_str}, 200

    

def print_all_accounts():
    conn = sqlite3.connect('accounts.db')
    c = conn.cursor()

    for row in c.execute('SELECT * FROM accounts ORDER BY username'):
        print(row)

    conn.close()

def switch_station_status(station_id, status):
    op_sql.switch_charging_station(station_id, status)

class TimeSystem:
    def __init__(self, start_time, time_unit, end_time,is_auto, step,wait_list):
        #time_unit表示时间系统的每个周期的长度如秒，分
        self.run_time = 0
        self.paused = True
        self.mode = "step" #初始化时间模式
        self.end_time = end_time
        self.current_time = start_time
        self.start_time = start_time
        self.time_unit = time_unit
        self.is_auto = is_auto
        self.step = step
        self.running = False  # 初始化 running 为 False
        self.wait_list = wait_list

    def run_until(self, run_time):
        self.run_time = run_time
        self.paused = True
        if not self.running:
            threading.Thread(target=self.step_forward).start()
    def stop(self):
        self.paused = True

    def update_charging_station(self, station_id, status, current_charging_car):
        # 连接到SQLite数据库
        conn = sqlite3.connect('charging_stations.db')

        # 创建一个Cursor对象
        c = conn.cursor()

        # 执行UPDATE语句
        c.execute("""
        UPDATE charging_stations
        SET status = ?, current_charging_car = ?, 
        WHERE station_id = ?
        """, (status, current_charging_car, station_id))

        # 提交事务
        conn.commit()

        # 关闭连接
        conn.close()

    def calculate_fee(self):
        current_hour = time_system.current_time
        # 判断当前时间属于哪个电价区间
        if 10 <= current_hour < 15 or 18 <= current_hour < 21:
            unit_price = 1.0  # 峰时电价
        elif 7 <= current_hour < 10 or 15 <= current_hour < 18 or 21 <= current_hour < 23:
            unit_price = 0.7  # 平时电价
        else:
            unit_price = 0.4  # 谷时电价

        # 充电费=单位电价*充电度数
        charging_fee = unit_price * self.charged_volume

            # 服务费=服务费单价*充电度数
        service_fee = self.SERVICE_FEE * self.charged_volume

            # 总费用=充电费+服务费
        total_fee = charging_fee + service_fee

        return total_fee

    def push_event_to_wait_list(self, wait_list, current_time, event_list):
        # event_list是一个链表，每个节点是一个事件，遍历链表，将所有event_time小于等于当前时间的事件加入等待队列
        current_node = event_list.head
        while current_node is not None:
            if current_node.event_time <= current_time:
                # add(self, car_id, charge_value, charge_mode)
                wait_list.add(current_node.car_id, current_node.charge_value, current_node.charge_mode)
                current_node = current_node.next

        event_list.removeByTime(current_time)


    def step_forward(self):
        print(f"Step forward running in thread {threading.current_thread().name}")
        self.running = True  # 开始运行
        while self.current_time < self.end_time:
            # 正常运行的代码...
            self.push_event_to_wait_list(wait_list, self.current_time, event_list)
            print("Before check_and_operate")
            self.check_and_operate()
            print("After check_and_operate")
            for station, cars in charging_cars.items():
                for car in cars:
                    car.charge(self.time_unit)
                    self.calculate_fee()
                    car.add_to_bill()
                    if car.is_charged():  # 如果车辆已经充电完成
                        cars.remove(car)  # 从正在充电的车辆列表中移除
                        self.update_charging_station(station, 'free', None)  # 将充电站状态更新为'free'
            self.current_time += self.step
            print(f"Current time in step forward: {self.current_time}")

            if self.current_time >= self.run_time or self.paused:
                self.paused = True
                print(f"Paused at {self.run_time}")
                break
        self.running = False  # 停止运行
        print('Finished step_forward method.')

    def auto_run(self):
        print(f"Auto run running in thread {threading.current_thread().name}")
        self.running = True  # 开始运行
        while self.current_time <= self.end_time:
            print(f"Current time: {self.current_time}")
            self.push_event_to_wait_list(wait_list, self.current_time, event_list)
            for _ in range(int(1 / self.time_unit)):
                self.check_and_operate()
                time.sleep(1)
            for station, cars in charging_cars.items():
                for car in cars:
                    car.charge(self.time_unit)
                    self.calculate_fee()
                    car.add_to_bill()
                    if car.is_charged():  # 如果车辆已经充电完成
                        cars.remove(car)  # 从正在充电的车辆列表中移除
                        self.update_charging_station(station, 'free', None)  # 将充电站状态更新为'free'
            self.current_time += self.step

            time.sleep(self.time_unit)
        self.running = False  # 停止运行

    def run(self):
            if self.running:  # 如果已经在运行，就直接返回
                return
            if self.mode == "step":
                thread = threading.Thread(target=self.step_forward)
            else:
                thread = threading.Thread(target=self.auto_run)
            thread.start()  # 在新的线程中运行 step_forward 或 auto_run 方法
    def check_and_operate(self):
        # 在这里添加每个时间单位开始时进行的检查和操作

        add_charging_car(self.wait_list)#把等待列表里的车添加到正在充电列表
        pass



@app.route('/run_until', methods=['POST'])
def run_until():
    data = request.get_json()
    hour = data['hour']
    print(f"Running until {hour}")
    time_system.run_time = hour
    time_system.paused = False  # 让step_forward方法重新开始运行
    if not time_system.running:
        threading.Thread(target=time_system.step_forward).start()
    return "200"

@app.route('/set_mode', methods=['POST'])
def set_mode():

    new_mode = request.json['mode']
    if new_mode in ["step", "auto"]:
        print(f'Before: mode = {time_system.mode}, running = {time_system.running}')
        time_system.running = False  # 停止当前的模式
        time.sleep(1)  # 等待一段时间让当前的模式完全停止
        time_system.mode = new_mode  # 切换到新的模式
        time_system.run()  # 开始运行新的模式
        print(f'After: mode = {time_system.mode}, running = {time_system.running}')
        return jsonify({'status': 'success'})

    else:
        return jsonify({'status': 'error', 'message': 'Invalid mode'}), 400


@app.route('/current_time', methods=['GET'])
def current_time():
    hours, remainder = divmod(time_system.current_time, 1)
    minutes = int(remainder * 60)
    return jsonify({'current_time': f'{int(hours):02d}:{minutes:02d}'})
def run_app():
    app.run(port=5000, debug=True)

time_system = TimeSystem(start_time, time_unit, end_time, is_auto, step, wait_list)
time_thread = threading.Thread(target=time_system.run)

time_thread.start()
run_app()


if __name__ == '__main__':

    # WaitingList.add(wait_list, 'lv1', 12, 'F')
    # WaitingList.add(wait_list, 'lv2', 13, 'T')
    # wait_list.print()
    # wait_list.getFirstFast().print()
    # wait_list.getFirstSlow().print()



    print_all_accounts()
