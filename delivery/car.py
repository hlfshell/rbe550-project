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

        v_max = 24 
        v_min = 12
        self.v = ((v_max-v_min)*random()) + v_min
   
        self.time = 0.0
        self.leg=1
        self.path_finished = False

      
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

        for node in self.path:
            pygame.draw.circle(surface, (255, 0 ,0), (node[0], node[1]), 5)
    
    def tick(self, time_delta: float):
        self.time += time_delta
        pixels_per_meter = 15
        prev_node = self.path[self.leg-1]
        next_node=self.path[self.leg]

        x_vector=(next_node[0]-prev_node[0])/pixels_per_meter
        y_vector=(next_node[1]-prev_node[1])/pixels_per_meter    
        theta_vector=next_node[2]-prev_node[2]
        dx=sqrt(x_vector**2+y_vector**2)

        turn_radius=min(abs(next_node[0]-prev_node[0]),abs(next_node[1]-prev_node[1]))/pixels_per_meter  #in meters
        turn_radius=40/15
        turn_circle=pi*2*turn_radius #pi d in meters

        #num_ticks=round(dx/time_delta,0)

        if theta_vector!=0:
            theta_dot=theta_vector/(turn_circle/4/self.v)  #radius/sec with direction
        else:
            theta_dot=0
        
        self.theta=self.theta+theta_dot*time_delta
        self.x=self.x+cos(self.theta)*self.v*time_delta
        self.y=self.y-sin(self.theta)*self.v*time_delta
        #self.x = self.x + x_vector/self.v*time_delta
        #self.y = self.y + y_vector/self.v*time_delta

        dx_to_next_leg=sqrt((next_node[0]/pixels_per_meter-self.x)**2+(next_node[1]/pixels_per_meter-self.y)**2)
        if dx_to_next_leg<=2*self.v*time_delta:
            self.x=next_node[0]/pixels_per_meter
            self.y=next_node[1]/pixels_per_meter
            self.theta=next_node[2]
            if self.leg<len(self.path)-1:
                self.leg+=1
            else:
                self.path_finished=True

CarPaths = [
    [(1650, 490,pi, []),
        (1420,490,pi,[44,33]),
        (1335,490,pi, [44,33]),
        (1295,450,pi/2, []),
        (1295,300,pi/2,[39,37]),
        (1295,200,pi/2, [39,37]),
        (1295,140,pi/2, []),
        (1255,100,pi, []),
        (880,100,pi, []),
        (840,60,pi/2, []),
        (840,-50,pi/2, [])],
    [(850,850,pi/2, []),
        (850,800,pi/2, [27,26]),
        (845,700,pi/2, [27,26]),
        (850,525,pi/2, []),
        (810,485,pi, []),
        (730,485,pi, [22,23]),
        (660,485,pi, [22,23]),
        (620,440,pi/2, []),
        (620,270,pi/2, [2,4]),
        (620,200,pi/2, [2,4]),
        (660,160,0, []),
        (1200,160,0, []),
        (1240,200,-pi/2, [37,39]),
        (1240,300,-pi/2, [37,39]),
        (1240,500,-pi/2, []),
        (1280,540,0, []),
        (1330,540,0, [44,33]),
        (1440,540,0, [44,33]),
        (1475,580,-pi/2, []),
        (1475,850,-pi/2, [])],
    [(-50,160,0, []),
        (140,160,0, []),
        (180,200,-pi/2, [5, 6]),
        (180,280,-pi/2, [5, 6]),
        (180,500,-pi/2, []),
        (220,540,0, []),
        (270,540,0, [13, 10]),
        (370,540,0, [13, 10]),
        (410,580,-pi/2, []),
        (410,850,-pi/2, [])] ,
    [(790,-50,-pi/2, []),
        (790,70,-pi/2, []),
        (750,110,-pi, []),
        (600,110,-pi, []),
        (560,150,-pi/2, [2, 4]),
        (560,280,-pi/2, [2, 4]),
        (560,450,-pi/2, []),
        (520,490,-pi, []),
        (350, 490, -pi, [13, 10]),
        (270,490,-pi, [13, 10]),
        (235,450,-3*pi/2, []),
        (235, 280, -3*pi/2, [5, 6]),
        (235, 200, -3*pi/2, [5, 6]),
        (235,-50,-3*pi/2, [])]
]
#     [(1650, 490,pi), #tstarting at 4 oclock coming left
#         (1335,490,pi),  #right turn to
#         (1295,455,pi/2),
#         (1295,140,pi/2),  #left turn to
#         (1255,100,pi),
#         (880,100,pi),  #right turn to
#         (840,60,pi/2),  
#         (840,-50,pi/2)],
#     [(850,850,pi/2),
#         (850,525,pi/2),
#         (810,485,pi),
#         (660,485,pi),
#         (620,440,pi/2),
#         (620,200,pi/2),
#         (660,160,0),
#         (1200,160,0),
#         (1240,200,-pi/2),
#         (1240,500,-pi/2),
#         (1280,540,0),
#         (1435,540,0),
#         (1475,580,-pi/2),
#         (1475,850,-pi/2)],
#     [(-50,160,0),
#         (140,160,0),
#         (180,200,-pi/2),
#         (180,500,-pi/2),
#         (220,540,0),
#         (370,540,0),
#         (410,580,-pi/2),
#         (410,850,-pi/2)] ,
#     [(790,-50,-pi/2),
#         (790,70,-pi/2),
#         (750,110,-pi),
#         (600,110,-pi),
#         (560,150,-pi/2),
#         (560,450,-pi/2),
#         (520,490,-pi),
#         (275,490,-pi),
#         (235,450,-3*pi/2),
#         (235,-50,-3*pi/2)]
# ]