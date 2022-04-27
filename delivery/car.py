from random import choice, randint, random
from math import degrees, sqrt, cos, sin, pi
from typing import List, Tuple

import pygame


class Car():

    def __init__(
        self,
        path: List[Tuple[float, float, float]]
    ):
        self.path = path.copy()
        if randint(0, 1):
            path.reverse()

        pixels_per_meter = 15
        self.x = self.path[0][0] / pixels_per_meter
        self.y = self.path[0][1] / pixels_per_meter
        self.theta = self.path[0][2]

        v_max = 12
        v_min = 6
        self.v = ((v_max-v_min)*random()) + v_min

        self.time = 0.0

        self.path_finished = False

        self.path_times: List[float] = [0.0]
        first = path.pop(0)
        second = path.pop(0)
        while True:
            distance_between = sqrt(
                (first[0] - second[0])**2 +
                (first[1] - second[1])**2
            )
            time_to_travel = distance_between / self.v
            self.path_times.append(time_to_travel)
            first = second
            if len(path) == 0:
                break
            second = path.pop(0)

        type = choice(["a", "b", "c"])
        self.image = pygame.image.load(
            f"./delivery/img/car_{type}.png"
        ).convert_alpha()
    
    @property
    def pixel_xy(self):
        pixels_per_meter = 15
        return (
            round(self.x * pixels_per_meter),
            round(self.y * pixels_per_meter)
        )

    def render(self):
        angle = degrees(self.theta)
        self.sprite = pygame.transform.rotate(
            self.image,
            angle
        )
        self.rect = self.sprite.get_rect(center=self.pixel_xy)
        self.mask = pygame.mask.from_surface(self.sprite)
    
    def blit(self, surface: pygame.Surface):
        surface.blit(self.sprite, self.rect)
    
    def tick(self, time_delta: float):
        # First we find what node we should be starting
        # from.
        self.time += time_delta

        for index, t in enumerate(self.path_times):
            if self.time < t:
                break
        
        # If we are at the end, this car is finished
        if index == len(self.path_times) - 1:
            self.path_finished = True
            return
        
        # We actually want the prior index
        index = index - 1

        node = self.path[0]

        pixels_per_meter = 15

        x = node[0] / pixels_per_meter
        y = node[1] / pixels_per_meter
        theta = node[2]

        self.x = x + (self.v*time_delta)*cos(self.theta)
        self.y = y + (self.v*time_delta)*sin(self.theta)
        self.theta = theta


CarPaths = [
    [(1700, 485,-pi),
        (1360,485,-pi),
        (1300,430,0),
        (1300,150,0),
        (1200,100,-pi),
        (880,100,-pi),
        (850,60,0),
        (850,-100,0)],
    [(845,900,0),
        (845,530,0),
        (790,480,-pi/2),
        (650,480,-pi/2),
        (620,440,0),
        (620,210,0),
        (670,160,pi/2),
        (1200,160,pi/2),
        (1240,210,pi),
        (1240,500,pi),
        (1300,540,pi/2),
        (1430,540,pi/2),
        (1475,585,pi),
        (1475,900,pi)],
    [(-100,160,pi/2),
        (130,160,pi/2),
        (180,200,pi),
        (180,510,pi),
        (230,540,pi/2),
        (360,540,pi/2),
        (410,590,pi),
        (410,900,pi)],
    [(790,-100,-pi),
        (790,60,-pi),
        (750,100,-pi/2),
        (610,100,-pi/2),
        (560,150,-pi),
        (560,440,-pi),
        (520,490,-pi/2),
        (275,490,-pi/2),
        (235,440,-pi),
        (235,-100,-pi)]
]