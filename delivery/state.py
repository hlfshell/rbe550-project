from __future__ import annotations

from math import cos, pi, sin, sqrt
from typing import List, Optional, Tuple

from numpy import arange

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
        self.r = 1.0 # Wheel radius in meters
        self.L = 1.0 # ???
    
    def get_neighbors(self, time_delta: float) -> List[State]:
        neighbors: List[State] = []

        v_max = self.v_max

        for v_left in arange(-v_max, v_max, v_max/2):
            for v_right in arange(-v_max, v_max, v_max/2):
                state = self.forward_kinematics(v_left, v_right, time_delta)
                neighbors.append(state)

        return neighbors

    def forward_kinematics(self, v_left: float, v_right: float, time_delta: float) -> State:
        thetadot = (self.r/self.L)*(v_right - v_left)
        thetadelta = thetadot * time_delta
        theta = self.theta + thetadelta

        xdot = (self.r/2) * (v_left + v_right)*cos(theta)
        ydot = (self.r/2) * (v_left + v_right)*sin(theta)
        xdelta = xdot * time_delta
        ydelta = ydot * time_delta

        x = self.x + xdelta
        y = self.y + ydelta

        state = State(x, y, theta, xdot=xdot, ydot=ydot, thetadot=thetadot)
        return state

    def connects(self, other: State, time_delta: float) -> Optional[State]:
        distance = self.distance_between(other)
        max_distance = self.v_max * time_delta
        if distance > max_distance:
            return None

        # Ok, so it's possible. Let's calcultae the wheel
        # velocities needed to make this move.
        xdelta = other.x - self.x
        ydelta = other.y - self.y
        thetadelta = other.theta - self.theta

        xdot = xdelta / time_delta
        ydot = ydelta / time_delta
        thetadot = thetadelta / time_delta

        v_left = ((2*xdot)/(self.r*cos(other.theta))) - ((thetadot * self.L)/self.r)
        v_right = ((thetadot*self.L)/self.r) + v_left

        if abs(v_left) > self.v_max or abs(v_right) > self.v_max:
            return None
        else:
            state = other.clone()
            state.xdot = xdot
            state.ydot = ydot
            state.thetadot = thetadot
            return state

    def distance_between(self, other: State) -> float:
        return sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

    def transition_cost(self, other: State) -> float:
        distance = self.distance_between(other)
        theta_difference = abs(self.theta - other.theta)
        if theta_difference > pi:
            theta_difference = (2*pi) - theta_difference
        return distance + 4*(theta_difference)

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
    
    @property
    def pixel_xy(self) -> Tuple[int, int]:
        pixels_per_meter = 15
        return (self.x * pixels_per_meter, self.y * pixels_per_meter)
    
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
    
    def __hash__(self) -> int:
        return hash(
            (self.x, self.y, self.theta, self.xdot, self.ydot, self.thetadot)
        )
    
    def __lt__(self, other: State) -> bool:
        if other is None:
            return False
        return (self.x, self.y, self.theta) < \
            (other.x, other.y, other.theta)