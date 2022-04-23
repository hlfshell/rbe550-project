from __future__ import annotations
from math import degrees, pi

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
    
    def tick(self, time_delta: float):
        pass