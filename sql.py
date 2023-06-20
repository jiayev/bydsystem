
import sqlite3

def create_charging_stations_table():
    # 连接到数据库（如果不存在，将会创建一个新的数据库）
    conn = sqlite3.connect('charging_stations.db')

    # 创建一个Cursor对象
    c = conn.cursor()

    # 创建一个新的表
    c.execute('''
        CREATE TABLE charging_stations
        (station_id TEXT PRIMARY KEY,
         station_type TEXT,
         status TEXT,
         current_charging_car TEXT,
         charging_queue TEXT,
         current_waiting_car TEXT,
         on_service TEXT)
    ''')

        #事件表
    c.execute('''
        CREATE TABLE event_list
        (event_id TEXT PRIMARY KEY,
         event_type TEXT,
         charge_type TEXT,
         event_value TEXT,
         event_time TEXT
         )
    ''')

    #队列表
    c.execute('''
        CREATE TABLE wait_queue
        (queue_id TEXT PRIMARY KEY,
         queue_value TEXT,
         queue_type TEXT,
         queue_order TEXT
         )
    ''')

    #详单表
    c.execute('''
        CREATE TABLE detail_bill
        ( detail_id TEXT PRIMARY KEY,
         car_id TEXT,
         detail_time TEXT,
         charge_id TEXT,
         charge_sum TEXT,
         chatge_time TEXT,
         start_time TEXT,
         end_time TEXT,
         charge_fee TEXT,
         server_fee TEXT,
         total_fee TEXT
         )
    ''')

     #账单表
    c.execute('''
        CREATE TABLE bill
        (car_id TEXT,
         bill_id TEXT PRIMARY KEY,
         bill_time TEXT,
         charge_sum TEXT,
         charge_time TEXT,
         start_time TEXT,
         end_time TEXT,
         charge_fee TEXT,
         server_fee TEXT,
         total_fee TEXT,
         detail_list TEXT
         )
    ''')

    # 初始插入充电桩数据，其中 station_id 是唯一的，分别为 A, B, C, D, E
    stations = [("A", "fast", "free", "", "", "", "1"),
                ("B", "fast", "free", "", "", "", "1"),
                ("C", "slow", "free", "", "", "", "1"),
                ("D", "slow", "free", "", "", "", "1"),
                ("E", "slow", "free", "", "", "", "1")]

    c.executemany('''
        INSERT INTO charging_stations VALUES (?,?,?,?,?,?,?)
    ''', stations)

    # 提交事务
    conn.commit()

    # 关闭到数据库的连接
    conn.close()

if __name__ == "__main__":
    create_charging_stations_table()
    # requircs()