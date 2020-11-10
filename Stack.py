from LinkedList import LinkedList

class Stack:

    class TopElementError(Exception):
        def __init__(self):
            super().__init__("Stack is empty")

    def __init__(self):
        self.__items = LinkedList()

    def __repr__(self):
        return repr(self.__items)
    
    def is_empty(self):
        return self.__items.size() == 0
    
    def push(self, element):
        self.__items.add(element)
    
    def pop(self):
        if self.is_empty():
            raise self.TopElementError()
        element = self.__items[-1]
        del self.__items[-1]
        return element
    
    def peek(self):
        if self.is_empty():
            raise self.TopElementError()
        return self.__items[-1]
    
