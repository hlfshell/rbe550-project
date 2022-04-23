from __future__ import annotations

from math import pi, sqrt
from typing import List

class State():

    def __init__(
        self,
        x: float,
        y: float,
        theta: float,
        exact = False,
        xdot: float = 0.0,
        ydot: float = 0.0,
        thetadot: float = 0.0
    ):
        self.x = x
        self.y = y
        self.theta = theta

        self.theta = self.theta % (2*pi)

        if not exact:
            self.x = round(self.x, 1)
            self.y = round(self.y, 1)
            self.theta = round(self.theta, 1)
        
        self.xdot = xdot
        self.ydot = ydot
        self.thetadot = thetadot

        # Kinematic constants here
        self.v_max = 1.0
    
    def get_neighbors(self, time_delta: float) -> List[State]:
        neighbors: List[State] = []

        v_max = self.v_max

        for v_left in range(-v_max, v_max, v_max/2):
            for v_right in range(-v_max, v_max, v_max/2):
                state = self.forward_kinematics
                neighbors.append(state)

        return neighbors
        

    def forward_kinematics(self, v_left: float, v_right: float) -> State:
        pass

    def distance_between(self, other: State) -> float:
        return sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

    def transition_cost(self, other: State) -> float:
        distance = self.distance_between(other)
        theta_difference = abs(self.theta - other.theta)
        if theta_difference > pi:
            theta_difference = (2*pi) - theta_difference
        return distance + 4*(theta_difference)
    
    def connects(self, other: State, time_delta) -> bool:
        distance = self.distance_between(other)
        max_distance = self.v_max * time_delta
        if distance > max_distance:
            return False

        pass

    def clone(self):
        return State(
            self.x,
            self.y,
            self.theta,
            exact = True,
            xdot=self.xdot,
            ydot=self.ydot,
            thetadot=self.thetadot
        )
    
    def __eq__(self, other: State) -> bool:
        if other is None:
            return False
        distance = self.distance_between(other)
        stheta = self.theta % (2*pi)
        otheta = other.theta % (2*pi)
        theta_difference = abs(stheta - otheta)
        if theta_difference > pi:
            theta_difference = (2*pi) - theta_difference
        return distance < 0.5 and theta_difference < 0.1