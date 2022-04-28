from __future__ import annotations
from math import degrees, floor, pi

from typing import List
import pygame

from delivery.state import State


VEHICLE_SPRITE = "./delivery/img/robot.png"

class Vehicle(pygame.sprite.Sprite):

    def __init__(
        self,
        state: State,
    ):
        self.state = state
        self.pixels_per_meter = 15
        self.sprite: pygame.Surface = pygame.image.load(VEHICLE_SPRITE).convert_alpha()

        self.surface: pygame.Surface = None
        self.rect = pygame.Rect = None
        self.mask: pygame.mask.Mask = None

        self.path: List[State] = None
        self.path_time_delta: float = 0.0

        self.time = 0.0

        self.render()
        
    def render(self):
        # angle = -1*degrees(self.state.theta + (pi/2))
        angle = -1*degrees(self.state.theta)
        self.surface = pygame.transform.rotate(self.sprite, angle)
        xy = (self.state.x * self.pixels_per_meter, self.state.y * self.pixels_per_meter)
        self.rect = self.surface.get_rect(center=xy)
        self.mask = pygame.mask.from_surface(self.surface)

    def blit(self, display_surface: pygame.Surface):
        display_surface.blit(self.surface, self.rect)

    def clone(self) -> Vehicle:
        state = self.state.clone()
        return Vehicle(state)
    
    def set_path(self, path: List[State]):
        self.path = path
    
    def tick(self, time_delta: float, path_time_delta=2.0):
        if self.path is None or len(self.path) == 0:
            return

        self.time += time_delta

        index = floor(self.time / self.path_time_delta)

        # If we've reached the end, hold it
        if self.time >= path_time_delta * len(self.path) or \
            index >= len(self.path):
            self.state = self.path[-1]
            return
        
        state = self.path[index]

        xdelta = state.xdot * time_delta
        ydelta = state.ydot * time_delta
        thetadelta = state.thetadot * time_delta

        if thetadelta > pi:
            thetadelta = -1*((2*pi) - thetadelta)
        elif thetadelta < -pi:
            thetadelta = (2*pi) + thetadelta
        
        x = state.x + xdelta
        y = state.y + ydelta
        theta = state.theta + thetadelta

        self.state = State(
            x,
            y,
            theta,
            xdot = state.xdot,
            ydot = state.xdot,
            thetadot = state.thetadot
        )