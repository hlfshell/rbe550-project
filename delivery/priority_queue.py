from typing import Union
from queue import PriorityQueue
from delivery.state import State
from delivery.map import Node

class Queue():

    def __init__(self):
        self.queue = PriorityQueue()
    
    def push(self, value: Union[State, Node], cost=0):
        self.queue.put((cost, value))

    def pop(self) -> Union[State, Node]:
        return self.queue.get()[1]

    def __len__(self):
        return len(self.queue.queue)