from __future__ import annotations
from math import pi, degrees
from typing import List, Tuple
import pygame


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
            Obstacle('dumpster', (740,307), 0),
            Obstacle('dumpster', (335,600), 0),
            Obstacle('dumpster', (715,600), 0),
            Obstacle('trashcan', (1360,437), 0),
            Obstacle('trashcan', (1344,100), 0),
            Obstacle('trashcan', (400,442), 0),
            Obstacle('trashcan', (1550,460), 0),
            Obstacle('trashcan', (1200,560), 0),
            Obstacle('trashbag', (732,205), 0),
            Obstacle('trashbag', (262,80), 0),
            Obstacle('trashbag', (810,190), 0),
            Obstacle('trashcan', (516,140), 0),
            Obstacle('trashcan', (650,330), 0),
            Obstacle('bike', (1440,640), 0),
            Obstacle('bike', (1580,250), 0),
            Obstacle('bike', (1440,720), 0),
            Obstacle('bike', (890,445), 0),
            Obstacle('cone', (870,750), 0),
            Obstacle('cone', (765,735), 0),
            Obstacle('cone', (1215,215), 0),
            Obstacle('cone', (1270,230), 0),
            Obstacle('cone', (1327,255), 0),
            Obstacle('cone', (540,225), 0),
            Obstacle('cone', (540,270), 0),
            Obstacle('cone', (205,235), 0),
            Obstacle('cone', (150,220), 0)
        ]

    @staticmethod
    def Load_Sprite(type: str) -> pygame.surface.Surface:
        return pygame.image.load(
            f"./delivery/img/{type}.png"
        ).convert_alpha()