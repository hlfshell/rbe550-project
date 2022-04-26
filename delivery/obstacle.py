from __future__ import annotations
from math import pi, degrees
from typing import List, Tuple
import pygame

def _sprite(type: str):
    return 

class Obstacle(pygame.sprite.Sprite):
    def __init__(
        self,
        type: str,
        xy: Tuple[float, float],
        theta: float
    ):
        self.xy = xy
        self.theta = theta
        self.type = type

        self.sprite = Obstacle.Load_Sprite(self.type)
        self.sprite = pygame.transform.rotate(
            self.sprite,
            degrees(self.theta)
        )
        self.rect = self.sprite.get_rect(center=xy)
        self.mask = pygame.mask.from_surface(self.sprite)

    def render(self, surface: pygame.Surface):
        surface.blit(self.sprite, self.rect)

    @staticmethod
    def Load_Obstacles() -> List[Obstacle]:
        return [
            Obstacle("cone", (100, 100), pi/4)
        ]

    @staticmethod
    def Load_Sprite( type: str) -> pygame.sprite.Sprite:
        return pygame.image.load(
            f"./delivery/img/{type}.png"
        ).convert_alpha()