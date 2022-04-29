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
        #if randint(0, 1):
        #    path.reverse()

        pixels_per_meter = 15
        self.x = self.path[0][0] / pixels_per_meter
        self.y = self.path[0][1] / pixels_per_meter
        self.theta = self.path[0][2]

        v_max = 12 
        v_min = 6
        self.v = ((v_max-v_min)*random()) + v_min
   
        self.time = 0.0
        self.leg=1
        self.path_finished = False

        #self.path_times: List[float] = [0.0]
        #first = path.pop(0)
        #second = path.pop(0)
        #while True:
            # first_xy = (
            #     first[0] / pixels_per_meter,
            #     first[1] / pixels_per_meter
            # )
            # second_xy = (
            #     second[0] / pixels_per_meter,
            #     second[1] / pixels_per_meter
            # )
            # distance_between = sqrt(
            #     (first_xy[0] - second_xy[0])**2 +
            #     (first_xy[1] - second_xy[1])**2
            # )
            # time_to_travel = distance_between / self.v
            # time_at = time_to_travel + self.path_times[-1]
            # self.path_times.append(time_at)
            # first = second
            # if len(path) == 0:
            #     break
            # second = path.pop(0)

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
        angle = degrees(self.theta-pi/2)
        self.sprite = pygame.transform.rotate(
            self.image,
            angle
        )

        self.rect = self.sprite.get_rect(center=self.pixel_xy)
        self.mask = pygame.mask.from_surface(self.sprite)

    def blit(self, surface: pygame.Surface):
        surface.blit(self.sprite, self.rect)
    
    def tick(self, time_delta: float):
        self.time += time_delta
        pixels_per_meter = 15
        prev_node = self.path[self.leg-1]
        next_node=self.path[self.leg]

        x_vector=(next_node[0]-prev_node[0])/pixels_per_meter
        y_vector=(next_node[1]-prev_node[1])/pixels_per_meter    
        theta_vector=next_node[2]-prev_node[2]
        dx=sqrt(x_vector**2+y_vector**2)

        num_ticks=round(dx/time_delta,0)
        
        self.theta=self.theta+theta_vector/num_ticks
        self.x = self.x + x_vector/num_ticks
        self.y = self.y + y_vector/num_ticks

        dx_to_next_leg=sqrt((next_node[0]/pixels_per_meter-self.x)**2+(next_node[1]/pixels_per_meter-self.y)**2)
        if dx_to_next_leg<=self.v*time_delta:
            self.x=next_node[0]/pixels_per_meter
            self.y=next_node[1]/pixels_per_meter
            if self.leg<len(self.path)-1:
                self.leg+=1
            else:
                self.path_finished=True

CarPaths = [
    [(1650, 490,pi),
        (1330,490,pi),
        (1295,450,pi/2),
        (1295,160,pi/2),
        (1200,100,pi),
        (850,100,pi),
        (830,60,pi/2),
        (830,-50,pi/2)],
    [(845,850,pi/2),
        (845,530,pi/2),
        (790,485,pi),
        (650,485,pi),
        (620,440,pi/2),
        (620,180,pi/2),
        (670,160,0),
        (1200,160,0),
        (1244,180,-pi/2),
        (1244,500,-pi/2),
        (1300,540,0),
        (1440,540,0),
        (1475,585,-pi/2),
        (1475,850,-pi/2)],
    [(-50,160,0),
        (140,160,0),
        (180,200,-pi/2),
        (180,510,-pi/2),
        (230,540,0),
        (370,540,0),
        (410,590,-pi/2),
        (410,850,-pi/2)] ,
    [(790,-50,-pi/2),
        (790,75,-pi/2),
        (750,110,-pi),
        (610,110,-pi),
        (560,150,-pi/2),
        (560,440,-pi/2),
        (520,490,-pi),
        (270,490,-pi),
        (235,440,-3*pi/2),
        (235,-50,-3*pi/2)]
]