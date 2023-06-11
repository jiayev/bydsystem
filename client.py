import requests

# 设置服务器的基础URL
BASE_URL = 'http://localhost:5000'

def register(username, password, isadmin):
    # 使用POST请求发送用户注册信息到服务器
    response = requests.post(f'{BASE_URL}/register', data={'username': username, 'password': password, 'isadmin': isadmin})

    # 返回服务器的响应
    if response.status_code == 200:
        print('Registration successful.')
        return True
    else:
        print('Registration failed.')
        return False
def login(username, password):
    # 使用POST请求发送用户登录信息到服务器
    response = requests.post(f'{BASE_URL}/login', data={'username': username, 'password': password})

    # 返回服务器的响应
    if response.status_code == 200:
        print('Login successful.')
        return 1
    elif response.status_code == 201:
        print('Login successful, admin.')
        return 2
    else:
        print('Login failed.')
        return 0

charging_requests = {}


def charging_request(vehicle_id, charging_mode, charging_volume):
    response = requests.post(
        f'{BASE_URL}/charging_request',
        json={'vehicle_id': vehicle_id, 'charging_mode': charging_mode, 'charging_volume': charging_volume}
    )
    print(f'Response status: {response.status_code}')
    print(f'Response content: {response.content}')
    if response.status_code == 200:
        print(response.json()['message'])
    else:
        print('Charging request failed.')

def charging_detail(username):
    response = requests.get(f'{BASE_URL}/charging_detail', data={'username': username})
    print(response.json())

def charging_stations_inf():
    response = requests.get(f'{BASE_URL}/charging_stations_inf')
    #将回复消息用制表符修改，去除原有标点，输出为表格形式
    print('Charging stations information:')
    print('ID\tType\tStatus\tCharging\tWaiting\tOn Service')
    for i in response.json()['message'].split('\n'):
        print(i.replace('(', '').replace(')', '').replace(',', '\t').replace("'", ''))

def get_bill(username):
    response = requests.get(f'{BASE_URL}/get_bill', data={'username': username})
    print(response.json()['message'])

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

def main():
    username = None
    admin = False
    # 未登录或者登录的是非管理员账户时显示的菜单
    while True:
        print("\nCurrent Status:")
        if username is None: print("Not logged in.")
        else: 
            print(f"Logged in as {username}.")
            if admin: print("You are an admin.")
        print("\nWelcome to the EV Charging System! Please select an option:")
        print("1. Register")
        if username is None:
            print("2. Login")
        else:
            print("2. Logout")
        print("3. Submit a charging request")
        print("4. View Charging Stations Usage")
        print("5. Exit")
        if admin:
            print("6. Start/Stop Charging Station")
            print("7. Get Waiting Cars List")
            print("8. Get Report")
        if username is not None:
            print("b. Check Bill")


        option = input("\nEnter option number: ")

        if option == "1":
            rusername = input('Enter username: ')
            rpassword = input('Enter password: ')
            risadmin = False
            #type y or n to determine whether the user is an admin, risadmin is a boolean value
            risadmin = input("Are you an admin? (y/n)")
            register(rusername,rpassword,risadmin)
        elif option == "2":
            if username is None:
                admin = False 
                username = input('Enter username: ')
                password = input('Enter password: ')
                result = login(username, password)
                #如果登录失败，则username为None
                if result == 0:
                    username = None
                if result == 2:
                    admin = True
            else:
                username = None
                admin = False
                print("Logout successful.\n")
        elif option == "3":
            if username is None:
                print("Please login first.")
            else:
                vehicle_id = input('Enter your vehicle ID: ')
                charging_mode = input('Enter charging mode (fast or slow): ')
                charging_volume = float(input('Enter charging volume: '))
                charging_request(vehicle_id, charging_mode, charging_volume)
        elif option == "4":
           # if username is None:
           #     print("Please login first.")
            #else:
                charging_stations_inf()
                
        elif option == "5":
            print("Exiting... Thank you!")
            break

        elif option == "6":
            if username is None:
                print("Please login first.")
            elif not admin:
                print("You are not an admin.")
            else:
                station_id = input('Enter station ID: ')
                action = input('Enter action (start or stop): ')
                if action == 'start':
                    start_charger(station_id)
                elif action == 'stop':
                    stop_charger(station_id)

        elif option == "7":
            if username is None:
                print("Please login first.")
            elif not admin:
                print("You are not an admin.")
            else:
                get_waiting_vehicles()

        elif option == "8":
            if username is None:
                print("Please login first.")
            elif not admin:
                print("You are not an admin.")
            else:
                get_reports()

        elif option == "b":
            if username is None:
                print("Please login first.")
            else:
                get_bill(username)

        else:
            print("Invalid option. Please enter a valid option number.")
        


if __name__ == "__main__":
    main()