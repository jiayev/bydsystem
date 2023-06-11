import time
import traceback
import sqlite3
from sqlite3 import Error
from flask import Flask, request
import threading
from models import datetime
import queue

# 创建两个队列，一个用于快充的请求，另一个用于慢充的请求
fast_charging_queue = queue.Queue(maxsize=6)
slow_charging_queue = queue.Queue(maxsize=6)

app = Flask(__name__)

charging_requests = {}
charging_cars = {}
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
                 (username text, password text)''')

    conn.commit()
    conn.close()
@app.route('/register', methods=['POST'])
def register_account():
    username = request.form.get('username')  # 使用request.form获取POST数据
    password = request.form.get('password')

    conn = sqlite3.connect('accounts.db')
    c = conn.cursor()

    c.execute("INSERT INTO accounts VALUES (?,?)", (username, password))

    conn.commit()
    conn.close()
    return "Registration successful.", 200  # 确保注册成功后，返回200状态码

def check_account(username, password):
    conn = sqlite3.connect('accounts.db')
    c = conn.cursor()

    c.execute("SELECT * FROM accounts WHERE username=? AND password=?", (username, password))
    result = c.fetchone()

    conn.close()

    if result is None:
        return False
    else:
        return True


@app.route('/login', methods=['POST'])

def login():
    username = request.form.get('username')  # 从请求中获取用户名
    password = request.form.get('password')  # 从请求中获取密码

    if check_account(username, password):  # 如果 check_account 函数返回 True
        return "Login successful.", 200  # 返回登录成功消息和 200 状态码
    else:  # 如果 check_account 函数返回 False
        return "Invalid username or password.", 401  # 返回错误消息和 401 状态码




@app.route('/charging_request', methods=['POST'])
def charging_request():
    request_data = request.get_json()
    vehicle_id = request_data['vehicle_id']
    charging_mode = request_data['charging_mode']
    charging_volume = request_data['charging_volume']

    try:
        conn = sqlite3.connect('charge.db')
        conn2 = sqlite3.connect('charging_stations.db')
        # 分配一个充电桩
        assigned_station = assign_charging_station(conn2, vehicle_id, charging_mode)

        # 如果没有可用的充电桩，返回错误信息
        if assigned_station is None:
            return {"status": "fail", "message": "All charging stations are currently full."}, 400

        c = conn.cursor()
        c2 = conn2.cursor()

        c.execute(
            f"INSERT INTO charging_cars(vehicle_id, charging_volume, charged_volume, charging_mode, charging_station) VALUES ('{vehicle_id}', {charging_volume}, 0, '{charging_mode}', '{assigned_station}')")


        conn2.commit()
        conn2.close()
        conn.commit()
        conn.close()

        if is_charging_station_free(assigned_station):
            charge_and_bill(vehicle_id, assigned_station, charging_volume)

        # 返回成功信息和分配的电桩
        response = {"status": "success",
                    "message": f"Charging request received. Your vehicle has been assigned to charging station {assigned_station}."}

        return response, 200


    except Exception as e:

        print("Error occurred:", e)

        print("Full traceback:")

        traceback.print_exc()

        return {"status": "fail", "message": "An error occurred while processing your request."}, 500

def is_charging_station_free(charging_station):
    # 连接到你的数据库
    conn = sqlite3.connect('charging_stations.db')

    # 创建一个Cursor对象
    c = conn.cursor()

    # 执行SQL查询来获取指定充电桩的状态
    c.execute('SELECT status FROM charging_stations WHERE station_id = ?', (charging_station,))

    # 获取查询结果
    result = c.fetchone()

    # 检查结果
    if result is None:
        # 如果没有找到指定的充电桩，那么抛出一个错误
        raise ValueError("Invalid charging station ID")

    # 如果充电桩的状态是"free"，那么返回True，否则返回False
    return result[0] == 'free'



def charge_and_bill(conn, car_id, required_charge, charging_station_id):
    # 根据电价时段确定单位电价
    current_hour = datetime.now().hour
    if 10 <= current_hour < 15 or 18 <= current_hour < 21:
        unit_price = 1.0  # 峰时电价
    elif 7 <= current_hour < 10 or 15 <= current_hour < 18 or 21 <= current_hour < 23:
        unit_price = 0.7  # 平时电价
    else:
        unit_price = 0.4  # 谷时电价

    # 计算充电费
    charging_fee = unit_price * required_charge

    # 计算服务费
    service_fee_unit_price = 0.8  # 服务费单价
    service_fee = service_fee_unit_price * required_charge

    # 总费用 = 充电费 + 服务费
    total_fee = charging_fee + service_fee

    # 更新数据库中车辆的充电信息
    c = conn.cursor()
    c.execute("UPDATE cars SET charged=?, charging_fee=? WHERE id=?", (required_charge, total_fee, car_id))
    conn.commit()

    print(f"Car {car_id} has been charged at station {charging_station_id} for a total fee of {total_fee} yuan.")

    # 更新充电桩状态
    c.execute("UPDATE charging_stations SET status='free', current_charging_car='' WHERE station_id=?", (charging_station_id,))
    conn.commit()

    return total_fee

def get_charging_cars():
    # 返回一个列表，每个元素都是一个字符串，描述了一个正在充电的汽车的信息
    return [
        f'Car ID: {car_id}, Need charging volume: {info["need_charging_volume"]}, Charged volume: {info["charged_volume"]}, Charging mode: {info["charging_mode"]}'
        for car_id, info in charging_cars.items()
    ]

@app.route('/charging_detail', methods=['GET'])
def charging_detail():
    username = request.form['username']
    # 需要一些逻辑来生成和返回充电详单信息
    return {"message": "Charging detail returned successfully."}, 200

@app.route('/charging_stations', methods=['GET'])
def assign_charging_station(conn, car_id, charging_mode):
    c = conn.cursor()

    # 查询可用的充电桩
    c.execute("SELECT station_id FROM charging_stations WHERE status='free' AND station_type=?", (charging_mode,))
    free_stations = c.fetchall()

    # 如果没有可用的充电桩，返回None
    if not free_stations:
        return None

    # 选择一个可用的充电桩
    chosen_station = free_stations[0][0]

    # 更新数据库中的充电桩状态
    c.execute("UPDATE charging_stations SET status='occupied', current_charging_car=? WHERE station_id=?",
              (car_id, chosen_station))
    conn.commit()

    return chosen_station


def get_charging_stations():
    # 需要一些逻辑来返回所有充电桩状态信息
    return {"message": "Charging station information returned successfully."}, 200

def print_all_accounts():
    conn = sqlite3.connect('accounts.db')
    c = conn.cursor()

    for row in c.execute('SELECT * FROM accounts ORDER BY username'):
        print(row)

    conn.close()





if __name__ == '__main__':



    app.run(port=5000, debug=True)


    print_all_accounts()
