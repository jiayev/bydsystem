
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
         charging_queue TEXT)
    ''')

    # 初始插入充电桩数据，其中 station_id 是唯一的，分别为 A, B, C, D, E
    stations = [("A", "fast", "free", "", ""),
                ("B", "fast", "free", "", ""),
                ("C", "slow", "free", "", ""),
                ("D", "slow", "free", "", ""),
                ("E", "slow", "free", "", "")]

    c.executemany('''
        INSERT INTO charging_stations VALUES (?,?,?,?,?)
    ''', stations)

    # 提交事务
    conn.commit()

    # 关闭到数据库的连接
    conn.close()
# def requircs():
#     conn = sqlite3.connect('charging_stations.db')
#     #
#     #     # 创建一个Cursor对象
#     c = conn.cursor()
#     c.execute("SELECT * FROM charging_stations")
#     stations = c.fetchall()
#     for station in stations:
#         print(station)
if __name__ == "__main__":
    create_charging_stations_table()
    # requircs()