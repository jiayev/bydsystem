import requests

# 设置服务器的基础URL
BASE_URL = 'http://localhost:5000'

def register(username, password):
    # 使用POST请求发送用户注册信息到服务器
    response = requests.post(f'{BASE_URL}/register', data={'username': username, 'password': password})

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
        return True
    else:
        print('Login failed.')
        return False

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
    #一次输出的格式如：{'message': "('A', 'fast', 'occupied', '2', '')\n('B', 'fast', 'occupied', '1', '')\n('C', 'slow', 'occupied', '123', '')\n('D', 'slow', 'free', '', '')\n('E', 'slow', 'free', '', '')"}
    print(response.json()['message'])



def main():
    username = None
    while True:
        print("\nWelcome to the EV Charging System! Please select an option:")
        print("1. Register")
        print("2. Login")
        print("3. Submit a charging request")
        print("4. View Charging Stations Usage")
        print("5. Exit")

        option = input("\nEnter option number: ")

        if option == "1":
            rusername = input('Enter username: ')
            rpassword = input('Enter password: ')
            register(rusername,rpassword)
        elif option == "2":
            username = input('Enter username: ')
            password = input('Enter password: ')
            login(username, password)
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
        else:
            print("Invalid option. Please enter a valid option number.")


if __name__ == "__main__":
    main()