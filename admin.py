# 本文件废弃，功能已整合到client.py中
import requests

# 服务器基础URL
BASE_URL = 'http://127.0.0.1:5000'

# 注册管理员
def register_admin(username, password, isadmin):
    response = requests.post(f'{BASE_URL}/register_admin', json={'username': username, 'password': password, 'isadmin': isadmin})
    if response.status_code == 200:
        print('Registration successful.')
    else:
        print('Registration failed.')

# 管理员登录
def login_admin(username, password, isadmin):
    response = requests.post(f'{BASE_URL}/login_admin', json={'username': username, 'password': password, 'isadmin': isadmin})
    if response.status_code == 200:
        if isadmin:
            print('Login successful, admin.')
        else: print('Login successful.')
    else:
        print('Login failed.')

# 启动充电桩
def start_charger(charger_id):
    response = requests.post(f'{BASE_URL}/start_charger', json={'charger_id': charger_id})
    if response.status_code == 200:
        print('Charger started.')
    else:
        print('Charger start failed.')

# 关闭充电桩
def stop_charger(charger_id):
    response = requests.post(f'{BASE_URL}/stop_charger', json={'charger_id': charger_id})
    if response.status_code == 200:
        print('Charger stopped.')
    else:
        print('Charger stop failed.')

# 查看所有充电桩状态
def get_charger_status():
    response = requests.get(f'{BASE_URL}/charging_stations_status')
    if response.status_code == 200:
        print('Charger status:\n', response.json())
    else:
        print('Failed to get charger status.')

# 查看等待服务的车辆信息
def get_waiting_vehicles():
    response = requests.get(f'{BASE_URL}/waiting_vehicles')
    if response.status_code == 200:
        print('Waiting vehicles:', response.json())
    else:
        print('Failed to get waiting vehicles.')

# 查看报表
def get_reports():
    response = requests.get(f'{BASE_URL}/reports')
    if response.status_code == 200:
        print('Reports:', response.json())
    else:
        print('Failed to get reports.')
