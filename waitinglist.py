# 创建一个双向链表类，包含参数：car_id, charge_value, charge_mode
class WaitingNode:
    def __init__(self, car_id, charge_value, charge_mode):
        self.car_id = car_id
        self.charge_value = charge_value
        self.charge_mode = charge_mode
        self.next = None
        self.prev = None

    def print(self):
        print(self.car_id, self.charge_value, self.charge_mode)

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
    
    def print(self):
        current_node = self.head
        while current_node is not None:
            current_node.print()
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