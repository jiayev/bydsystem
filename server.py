import time
import traceback
import sqlite3
import waitinglist
from waitinglist import WaitingList
from waitinglist import WaitingNode
from sqlite3 import Error
from flask import Flask, request, g
import threading
from models import datetime, ChargingCar
import queue
import op_sql
import Timesys


# 创建两个队列，一个用于快充的请求，另一个用于慢充的请求
fast_charging_queue = queue.Queue(maxsize=6)
slow_charging_queue = queue.Queue(maxsize=6)

app = Flask(__name__)
# 全局的充电车辆列表
charging_cars = []

wait_list = WaitingList()
charging_requests = {}

# 创建一个 Event 对象
stop_charging_cars = threading.Event()




def display_charging_cars():
    while not stop_charging_cars.is_set():
        for id, car in charging_cars.items():
            print(f"Car ID: {id}")
            print(f"Required charge: {charging_requests[id]['charging_volume']}")
            print(f"Charged so far: {car['charged_volume']}")
            print(f"Charging mode: {charging_requests[id]['charging_mode']}")
            print()
        time.sleep(5)  # 每5秒打印一次

def create_account_table():
    conn = sqlite3.connect('accounts.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE accounts
                 (username text, password text, isadmin boolean)''')

    conn.commit()
    conn.close()
@app.before_first_request
def setup():
    wait_list = WaitingList()
    print("Waiting list created.\n")
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
        if value != 0:
            WaitingList.add(wait_list,id,value,charge_type)
        else:
            WaitingList.remove(wait_list,id)
    elif event_type == 'B':
            if op_sql.is_on_station(id) == value:
                return "Charging station is already on/off.", 400
            op_sql.turn_on_off_charging_station(id,value)
            if value == 1:
                return "Charging station is on.", 200
            else:
                return "Charging station is off.", 200
    elif event_type == 'C':
            WaitingList.changeInfo(wait_list,id,value,charge_type)

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

def add_charging_car(car_id, charging_mode, charging_volume):
    # 创建一个新的 ChargingCar 对象
    new_car = ChargingCar(car_id, charging_mode, charging_volume)

    # 将新的 ChargingCar 对象添加到 charging_cars 列表中
    charging_cars.append(new_car)

    # 返回新的 ChargingCar 对象
    return new_car


def is_charging_station_free(charging_station):
    return op_sql.is_busy_station(charging_station)

def push_list_to_charging_station(wait_list):
    return 200




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



if __name__ == '__main__':
   
    # WaitingList.add(wait_list, 'lv1', 12, 'F')
    # WaitingList.add(wait_list, 'lv2', 13, 'T')
    # wait_list.print()
    # wait_list.getFirstFast().print()
    # wait_list.getFirstSlow().print()
    app.run(port=5000, debug=True)
   
    
    print_all_accounts()
