
from typing import Dict, List, Optional

import pygame
from delivery.map import Map, Node
from delivery.priority_queue import Queue

MAX_STEPS = 500

class GlobalPlanner():

    def __init__(
        self,
        map: Map,
        start: Node,
        goal: Node
    ):
        self.map = map
        self.queue = Queue()
        self.start = start
        self.goal = goal

        self.queue.push(start)
        self.parents: Dict[Node, Node] = {start: None}
        self.costs: Dict[Node, float] = {}
        self.costs[self.start] = 0
        self.steps_taken = 0
    
    def search(self) -> List[Node]:
        path: Optional[List[Node]] = None

        while path == None:
            path = self.step()
            pygame.event.get()
            pygame.display.update()
        
        return path


    def step(self) -> Optional[List[Node]]:
        self.steps_taken += 1
        if self.steps_taken >= MAX_STEPS:
            raise Exception("Excessive steps in search for path in global planner")
        
        if len(self.queue) == 0:
            raise Exception("No such path to the goal exists")
        
        # Grab our next node in the prioritized queue
        current: Node = self.queue.pop()

        if self.goal == current:
            if current == self.start:
                return [current]
            path: List[Node] = [current]
            while True:
                current: Node  = self.parents[current]
                path.insert(0, current)
                if self.start == current:
                    return path

        neighbors = self.map.get_neighbors(current)
        for neighbor in neighbors:
            if neighbor not in self.parents:
                self.parents[neighbor] = current

                current_cost = self.costs[current]
                distance_to_goal = self.goal.distance_between(neighbor)
                distance_between = current.distance_between(neighbor)

                heuristic_cost = 5 * distance_to_goal

                node_cost = current_cost + distance_between

                total_cost = node_cost + heuristic_cost
                self.costs[neighbor] = total_cost

                self.queue.push(neighbor, total_cost)