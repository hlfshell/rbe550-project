from collections import defaultdict
from math import atan, atan2, degrees, pi, sqrt
from typing import Callable, Dict, List, Optional, Tuple

import pygame
from delivery.state import State
from delivery.priority_queue import Queue
from delivery.vehicle import Vehicle

MAX_STEPS = 20_000
SUCCESS_PROXIMITY_METERS = 0.25

class LocalPlanner():

    def __init__(
        self,
        start: State,
        goal: Tuple[float, float],
        time_delta: float,
        collision_detection: Callable,
        surface: pygame.Surface
    ):
        self.queue = Queue()
        self.start = start
        self.goal = goal
        self.time_delta = time_delta
        self.collision_detection = collision_detection
        self.surface = surface

        self.queue.push(start)
        self.parents: Dict[State, State] = { start: None }
        self.costs: Dict[State, float] = { start: 0 }
        self.exists = defaultdict(
            lambda: defaultdict(
                lambda: defaultdict(
                    lambda: False
                )
        ))
        self.steps_taken = 0
    
    def search(self) -> List[State]:
        path: Optional[List[State]] = None

        while path == None:
            path = self.step()
            pygame.event.get()
            pygame.display.update()
        
        return path
    
    def step(self) -> Optional[List[State]]:
        self.steps_taken += 1
        if self.steps_taken >= MAX_STEPS:
            raise Exception("Excessive steps in search for path in local planner")
        
        if len(self.queue) == 0:
            raise Exception("No such path to the goal exists")
        
        # Grab our next state to consider
        current: State = self.queue.pop()

        # Check to see if we've made it
        distance_between = sqrt(
            (current.x - self.goal[0])**2 +
            (current.y - self.goal[1])**2)
        if distance_between < SUCCESS_PROXIMITY_METERS:
            if current == self.start:
                return [current]
            path: List[State] = [current]
            while True:
                current: State = self.parents[current]
                path.insert(0, current)
                if self.start == current:
                    return path
        
        # We haven't found it yet, so let's generate kinematic
        # moves that we can consider later
        neighbors = current.get_neighbors(self.time_delta)
        for neighbor in neighbors:
            # If we have already reached this state, we don't
            # need to retread over this ground
            # x = round(0.05 * round(neighbor.x/0.05),2)
            # y = round(0.05 * round(neighbor.y/0.05),2)
            x = round(neighbor.x, 1)
            y = round(neighbor.y, 1)
            # theta = round(degrees(5) * round(neighbor.theta/degrees(5)),2)
            theta = round(neighbor.theta, 2)
            # print(">>", neighbor.x, neighbor.y, neighbor.theta, x, y, theta)
            if not self.exists[x][y][theta]:
            # if neighbor not in self.parents:
                # Check to see if this position is valid
                shadow = Vehicle(neighbor)
                if self.collision_detection(shadow):
                    continue

                self.parents[neighbor] = current
                self.exists[x][y][theta] = True

                distance_to_goal = sqrt(
                    (neighbor.x - self.goal[0])**2 +
                    (neighbor.y - self.goal[1])**2)
                distance_between = current.distance_between(neighbor)

                heading_to_goal = atan2(
                    (self.goal[1] - neighbor.y),
                    (self.goal[0] - neighbor.x))

                heading_difference = abs(heading_to_goal - neighbor.theta)
                heading_difference = heading_difference % (2*pi)
                if heading_difference > pi:
                    heading_difference = (2*pi) - heading_difference

                # heuristic_cost = (3 * distance_to_goal) + (0.5 * heading_difference)
                heuristic_cost = (2 * distance_to_goal) + (1 * heading_difference)
                node_cost = distance_between

                total_cost = node_cost + heuristic_cost
                # print(distance_to_goal, distance_between, heuristic_cost, node_cost, total_cost)
                self.costs[neighbor] = total_cost

                self.queue.push(neighbor, total_cost)
        
                # Draw a dot for the current considered spot
                self.surface.fill((0, 0, 255), (neighbor.pixel_xy, (4, 4)))