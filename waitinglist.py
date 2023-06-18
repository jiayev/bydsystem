# 创建一个双向链表类，包含参数：car_id, charge_value, charge_mode
import json


class WaitingNode:
    def __init__(self, car_id, charge_value, charge_mode):
        self.car_id = car_id
        self.charge_value = charge_value
        self.charge_mode = charge_mode
        self.next = None
        self.prev = None

    def print(self):
        print(self.car_id, self.charge_value, self.charge_mode)

    def getInfo(self):
        return self.car_id, self.charge_value, self.charge_mode

class WaitingList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def add(self, car_id, charge_value, charge_mode):
        new_node = WaitingNode(car_id, charge_value, charge_mode)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
            self.size += 1
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
            self.size += 1

    def remove(self, car_id):
        if self.head is None:
            return
        elif self.head.car_id == car_id:
            self.head = self.head.next
            self.size -= 1
        else:
            current_node = self.head
            while current_node.next is not None:
                if current_node.next.car_id == car_id:
                    current_node.next = current_node.next.next
                    self.size -= 1
                    break
                else:
                    current_node = current_node.next


    def get(self, car_id):
        current_node = self.head
        while current_node is not None:
            if current_node.car_id == car_id:
                return current_node
            else:
                current_node = current_node.next
        return None
    
    def getLength(self):
        return self.size
    
    def isExist(self, car_id):
        current_node = self.head
        while current_node is not None:
            if current_node.car_id == car_id:
                return True
            else:
                current_node = current_node.next
        return False

    def print(self):
        current_node = self.head
        while current_node is not None:
            current_node.print()
            current_node = current_node.next

    # 根据参数获取车辆信息
    def getInfo(self, car_id, attr):
        current_node = self.head
        while current_node is not None:
            if current_node.car_id == car_id:
                if attr == 'charge_value':
                    return current_node.charge_value
                elif attr == 'charge_mode':
                    return current_node.charge_mode
                else:
                    return None
            else:
                current_node = current_node.next

    def changeInfo(self, car_id, charge_value, charge_mode):
        current_node = self.head
        while current_node is not None:
            if current_node.car_id == car_id:
                current_node.charge_value = charge_value
                current_node.charge_mode = charge_mode
                break
            else:
                current_node = current_node.next

    # 将车辆移至队列尾部
    def moveToTail(self, car_id):
        current_node = self.head
        while current_node is not None:
            if current_node.car_id == car_id:
                if current_node == self.tail:
                    return
                elif current_node == self.head:
                    self.head = self.head.next
                    self.head.prev = None
                    self.tail.next = current_node
                    current_node.prev = self.tail
                    current_node.next = None
                    self.tail = current_node
                else:
                    current_node.prev.next = current_node.next
                    current_node.next.prev = current_node.prev
                    self.tail.next = current_node
                    current_node.prev = self.tail
                    current_node.next = None
                    self.tail = current_node
                break
            else:
                current_node = current_node.next

    def getFirstFast(self):
        current_node = self.head
        while current_node is not None:
            if current_node.charge_mode == 'F':
                return current_node
            else:
                current_node = current_node.next
        return None
    
    def getFirstSlow(self):
        current_node = self.head
        while current_node is not None:
            if current_node.charge_mode == 'T':
                return current_node
            else:
                current_node = current_node.next
        return None
    
# 创建一个单向链表类，作为事件，包含参数：事件类型（A,B,C）,发生时间（格式00:00）,车辆ID（任意字符串）,充电量（浮点）,充电模式（T,F,O）
class EventNode:
    def __init__(self, event_type, event_time, car_id, charge_value, charge_mode):
        self.event_type = event_type
        self.event_time = event_time
        self.car_id = car_id
        self.charge_value = charge_value
        self.charge_mode = charge_mode
        self.next = None

    def print(self):
        print(self.event_type, self.event_time, self.car_id, self.charge_value, self.charge_mode)

    def getInfo(self):
        return json.dumps({'event_type': self.event_type, 'event_time': self.event_time, 'car_id': self.car_id, 'charge_value': self.charge_value, 'charge_mode': self.charge_mode})
    
class EventList:
    def __init__(self):
        self.head = None
        self.size = 0

    def add(self, event_type, event_time, car_id, charge_value, charge_mode):
        new_node = EventNode(event_type, event_time, car_id, charge_value, charge_mode)
        if self.head is None:
            self.head = new_node
            self.size += 1
        else:
            current_node = self.head
            while current_node.next is not None:
                current_node = current_node.next
            current_node.next = new_node
            self.size += 1

    def remove(self):
        if self.head is None:
            return
        else:
            self.head = self.head.next
            self.size -= 1

    def getFirst(self):
        return self.head

    def getLength(self):
        return self.size

    def print(self):
        current_node = self.head
        while current_node is not None:
            current_node.print()
            current_node = current_node.next

    def getInfoByEach(self):
        current_node = self.head
        info = []
        while current_node is not None:
            info.append(current_node.getInfo())
            current_node = current_node.next
        return info
    
    def removeByTime(self, time):
        current_node = self.head
        while current_node is not None:
            if current_node.event_time <= time:
                if current_node == self.head:
                    self.head = self.head.next
                    self.size -= 1
                else:
                    current_node.prev.next = current_node.next
                    self.size -= 1
                break
            else:
                current_node = current_node.next

    def sortByTime(self):
        current_node = self.head
        while current_node is not None:
            next_node = current_node.next
            while next_node is not None:
                if current_node.event_time > next_node.event_time:
                    current_node.event_type, next_node.event_type = next_node.event_type, current_node.event_type
                    current_node.event_time, next_node.event_time = next_node.event_time, current_node.event_time
                    current_node.car_id, next_node.car_id = next_node.car_id, current_node.car_id
                    current_node.charge_value, next_node.charge_value = next_node.charge_value, current_node.charge_value
                    current_node.charge_mode, next_node.charge_mode = next_node.charge_mode, current_node.charge_mode
                next_node = next_node.next
            current_node = current_node.next

