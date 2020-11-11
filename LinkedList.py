class LinkedList:

    def __init__(self):
        self.num_items = 0
        self.first = None
        self.last = None
    
    def __repr__(self):
        rep = "["
        curr_node = self.first
        while curr_node:
            rep += repr(curr_node.payload)
            if curr_node.next:
                rep += ", "
            curr_node = curr_node.next
        rep += "]"
        return rep

    def size(self):
        return self.num_items

    def add(self, item):
        new_node = self.Node(item)
        if self.num_items == 0:
            self.first = new_node
        else:
            self.last.next = new_node
            new_node.prev = self.last
        self.last = new_node
        self.num_items += 1
    
    def insert(self, index, item):
        new_node = self.Node(item)
        if index == 0 or index <= -self.num_items:
            if self.num_items:
                self.first.prev = new_node
                new_node.next = self.first
            else:
                self.last = new_node
            self.first = new_node
        elif index < 0:
            curr_node = self.last
            for i in range(0, index, -1):
                curr_node = curr_node.prev
            new_node.next = curr_node.next
            curr_node.next.prev = new_node
            curr_node.next = new_node
            new_node.prev = curr_node
        elif index >= self.num_items:
            if self.num_items:
                self.last.next = new_node
                new_node.prev = self.last
            else:
                self.first = new_node
            self.last = new_node
        else:
            curr_node = self.first
            for i in range(1, index):
                curr_node = curr_node.next
            new_node.next = curr_node.next
            curr_node.next.prev = new_node
            curr_node.next = new_node
            new_node.prev = curr_node
        self.num_items += 1
    
    def __getitem__(self, index):
        if index >= self.num_items or index < -self.num_items:
            raise IndexError("LinkedList index out of range")
        
        if index < 0:
            curr_node = self.last
            for i in range(-1, index, -1):
                curr_node = curr_node.prev
        else:
            curr_node = self.first
            for i in range(index):
                curr_node = curr_node.next
        
        return curr_node.payload

    def __setitem__(self, index, item):
        if index >= self.num_items or index < -self.num_items:
            raise IndexError("LinkedList index out of range")
        
        if index < 0:
            curr_node = self.last
            for i in range(-1, index, -1):
                curr_node = curr_node.prev
        else:
            curr_node = self.first
            for i in range(index):
                curr_node = curr_node.next
        
        curr_node.payload = item

    def __delitem__(self, index):
        if index >= self.num_items or index < -self.num_items:
            raise IndexError("LinkedList index out of range")
        
        if index < 0:
            curr_node = self.last
            for i in range(-1, index, -1):
                curr_node = curr_node.prev
        else:
            curr_node = self.first
            for i in range(index):
                curr_node = curr_node.next
        
        if curr_node.prev:
            curr_node.prev.next = curr_node.next
            if curr_node.next:
                curr_node.next.prev = curr_node.prev
            else:
                self.last = curr_node.prev
        else:
            self.first = curr_node.next
            if curr_node.next:
                curr_node.next.prev = None
            else:
                self.last = None
        
        self.num_items -= 1
    
    def remove(self, item):
        curr_node = self.first
        while curr_node and curr_node.payload != item:
            curr_node = curr_node.next
        if curr_node:
            if curr_node.prev:
                curr_node.prev.next = curr_node.next
                if curr_node.next:
                    curr_node.next.prev = curr_node.prev
                else:
                    self.last = curr_node.prev
            else:
                self.first = curr_node.next
                if curr_node.next:
                    curr_node.next.prev = None
                else:
                    self.last = None
            self.num_items -= 1
        else:
            raise ValueError("LinkedList.remove(x): x not in LinkedList")

    class Node:
        def __init__(self, payload):
            self.payload = payload
            self.prev = None
            self.next = None
        
        def __repr__(self):
            return repr(self.payload)
