import sqlite3

#--------------------------------------------------------------------------------------------------------------------------------#
def query_station_all():
    #这个我只写了查询所有
    conn = sqlite3.connect('charging_stations.db')
    cursor = conn.execute('SELECT * FROM charging_stations')
    for row in cursor:
        print(row)
    conn.close() 

def nsert_charging_station(station_id, station_type, status, current_charging_car, charging_queue, current_waiting_car):
    #这个要传入所有参数，壕沟巴烦
    conn = sqlite3.connect('charging_stations.db')
    c = conn.cursor()
    c.execute("INSERT INTO charging_stations (station_id, station_type, status, current_charging_car, charging_queue, current_waiting_car) \
              VALUES (?, ?, ?, ?, ?, ?)", (station_id, station_type, status, current_charging_car, charging_queue, current_waiting_car))
    conn.commit()
    conn.close()

def delete_charging_station(station_id):
    #这个只需要传入station_id
    conn = sqlite3.connect('charging_stations.db')
    c = conn.cursor()
    c.execute("DELETE FROM charging_stations WHERE station_id = ?", (station_id,))
    conn.commit()
    conn.close()

def update_charging_station(station_id, station_type, status, current_charging_car, charging_queue, current_waiting_car):
    #这个更新station_id对应的列
    conn = sqlite3.connect('charging_stations.db')
    c = conn.cursor()
    c.execute("UPDATE charging_stations SET station_type = ?, status = ?, current_charging_car = ?, charging_queue = ?, current_waiting_car = ?  WHERE station_id = ?",  
              (station_type, status, current_charging_car, charging_queue, current_waiting_car, station_id))
    conn.commit()
    conn.close()  

#---------------------------------------------------------------------------------------------------------------------------#

def query_event_all():
    conn = sqlite3.connect('charging_stations.db')
    cursor = conn.execute('SELECT * FROM event_list')
    for row in cursor:
        print(row)
    conn.close() 

def insert_event(event_id, event_type, charge_type, event_value, event_time):
    #这个也要传入所有参数，壕沟巴烦
    conn = sqlite3.connect('charging_stations.db')
    c = conn.cursor()
    c.execute("INSERT INTO event_list (event_id, event_type, charge_type, event_value, event_time) \
              VALUES (?, ?, ?, ?, ?)", (event_id, event_type, charge_type, event_value, event_time))
    conn.commit()
    conn.close()

def delete_event(event_id):
    conn = sqlite3.connect('charging_stations.db')
    c = conn.cursor()
    c.execute("DELETE FROM event_list WHERE event_id = ?", (event_id,))
    conn.commit()
    conn.close() 


def update_event(event_id, event_type, charge_type, event_value, event_time):
    conn = sqlite3.connect('charging_stations.db')
    c = conn.cursor()
    c.execute("UPDATE event_list SET event_type = ?, charge_type = ?, event_value = ?, event_time = ?  WHERE event_id = ?",  
              (event_type, charge_type, event_value, event_time, event_id))
    conn.commit()
    conn.close()


#-------------------------------------------------------------------------------------------------------------------#

def query_queue_all():
    conn = sqlite3.connect('charging_stations.db')
    cursor = conn.execute('SELECT * FROM wait_queue')
    for row in cursor:
        print(row)
    conn.close() 

def insert_wait_queue(queue_id, queue_value, queue_type, queue_order):
    conn = sqlite3.connect('charging_stations.db')
    c = conn.cursor()
    c.execute("INSERT INTO wait_queue (queue_id, queue_value, queue_type, queue_order) \
              VALUES (?, ?, ?, ?)", (queue_id, queue_value, queue_type, queue_order))
    conn.commit()
    conn.close()

def delete_wait_queue(queue_id):
    conn = sqlite3.connect('charging_stations.db')
    c = conn.cursor()
    c.execute("DELETE FROM wait_queue WHERE queue_id = ?", (queue_id,))
    conn.commit()
    conn.close()

def update_wait_queue(queue_id, queue_value, queue_type, queue_order):
    conn = sqlite3.connect('charging_stations.db')
    c = conn.cursor()
    c.execute("UPDATE wait_queue SET queue_value = ?, queue_type = ?, queue_order = ?  WHERE queue_id = ?",  
              (queue_value, queue_type, queue_order, queue_id))
    conn.commit()
    conn.close()

#-------------------------------------------------------------------------------------------------------------------#

def query_queue_all():
    conn = sqlite3.connect('charging_stations.db')
    cursor = conn.execute('SELECT * FROM detail_bill')
    for row in cursor:
        print(row)
    conn.close() 

def insert_detail_bill(detail_id, car_id, detail_time, charge_id, charge_sum, chatge_time, 
                       start_time, end_time, charge_fee, server_fee, total_fee):
    conn = sqlite3.connect('charging_stations.db')
    c = conn.cursor()
    c.execute("INSERT INTO detail_bill (detail_id, car_id, detail_time, charge_id, charge_sum, chatge_time, start_time, end_time, charge_fee, server_fee, total_fee)  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",  
              (detail_id, car_id, detail_time, charge_id, charge_sum, chatge_time, start_time, end_time, charge_fee, server_fee, total_fee)) 
    conn.commit()
    conn.close()

def delete_detail_bill(detail_id):
    conn = sqlite3.connect('charging_stations.db')
    c = conn.cursor()
    c.execute("DELETE FROM detail_bill WHERE detail_id = ?", (detail_id,))
    conn.commit()
    conn.close()

def update_detail_bill(detail_id, car_id, detail_time, charge_id, charge_sum, chatge_time, 
                       start_time, end_time, charge_fee, server_fee, total_fee):
    #更新detail_id对应的列
    conn = sqlite3.connect('charging_stations.db')
    c = conn.cursor()
    c.execute("UPDATE detail_bill SET car_id = ?, detail_time = ?, charge_id = ?, charge_sum = ?, chatge_time = ?,  start_time = ?, end_time = ?, charge_fee = ?, server_fee = ?, total_fee = ?  WHERE detail_id = ?",  
              (car_id, detail_time, charge_id, charge_sum, chatge_time, start_time, end_time, charge_fee, server_fee, total_fee, detail_id))
    conn.commit()
    conn.close()
