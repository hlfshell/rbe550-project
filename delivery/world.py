from math import cos, pi, sin
from random import choice
from time import time
from typing import List
import pygame
from delivery.global_planner import GlobalPlanner
from delivery.local_planner import LocalPlanner
from delivery.map import Map, Node
from delivery.state import State

from delivery.vehicle import Vehicle


BG_SPRITE = "./delivery/img/map.png"
COLLISION_MAP = "./delivery/img/collision_map.png"
WINDOW_SIZE = (1600, 800)

class World:

    def __init__(self):
        self.window_size = WINDOW_SIZE
        self.pixels_per_meter = 15
        self._display_surface : pygame.Surface = None
        self._frame_per_sec = pygame.time.Clock()
        self._fps = 60

        self._display_surface: pygame.Surface = None
        self._obstacle_map: pygame.Surface = None
        self._map: pygame.Surface = None

        self.vehicle: Vehicle = None
        self.map = Map.Get_Map()

        self.global_path: List[Node] = None
        self.local_path: List[State] = None

        self._display_surface = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption("RBE550 Delivery Robot Project")

        self.bg_sprite: pygame.Surface = pygame.image.load(BG_SPRITE).convert_alpha()
        self.bg_sprite = pygame.transform.scale(self.bg_sprite, WINDOW_SIZE)

        self._collision_map: pygame.sprite.Group = pygame.sprite.Group()
        self._collision_map.add(CollisionMap())

        self.render()
    
    def render(self):
        # Draw background color
        pygame.Surface.fill(self._display_surface, (0, 0, 0))
        self._display_surface.blit(self.bg_sprite, self.bg_sprite.get_rect())

        self.map.render(self._display_surface)
        self.draw_global_path()

        if self.vehicle is not None:
            self.vehicle.render()
            self.vehicle.blit(self._display_surface)

    def draw_global_path(self):
        if self.global_path is None:
            return
        
        if len(self.global_path) <= 1:
            return
        
        color = (0, 255, 0)
        drawn = self.global_path.copy()
        first = drawn.pop(0)
        second  = drawn.pop(0)
        while True:
            pygame.draw.line(
                self._display_surface,
                color,
                first.pixel_xy,
                second.pixel_xy,
                width=3
            )
            first = second
            if len(drawn) == 0:
                break
            second = drawn.pop(0)

        pygame.display.update()

    def set_vehicle(self, vehicle: Vehicle):
        self.vehicle = vehicle

    def collision_detection(self, vehicle) -> bool:
        off_map_collisions = pygame.sprite.spritecollide(
            vehicle,
            self._collision_map,
            False,
            pygame.sprite.collide_mask
        )
        if len(off_map_collisions) > 0:
            return True
        return False
    
    def tick(self):
        pass

    def global_plan(self):
        goal = None
        while goal == None:
            node: Node = choice(list(self.map.nodes.values()))
            if node.type == "delivery":
                goal = node

        # goal = self.map.nodes[14]
        
        planner = GlobalPlanner(self.map, self.map.start, goal)
        self.global_path = planner.search()

    def test_global_planner(self):
        time_start: float = 0.0
        while True:
            if time() - time_start >= 1.0:
                self.global_plan()
                time_start = time()
            self.render()
            pygame.event.get()
    
    def test_local_planner(self):
        time_start: float = time()
        while True:
            if time() - time_start >= 3.0:
                self.global_plan()
                time_start = time()
            self.render()
            pygame.event.get()

            # Now we create local plan for each step
            if self.global_path is None:
                continue

            global_path = self.global_path.copy()
            print("got global path", global_path)
            current_node = global_path.pop(0)
            current_vehicle_state = self.vehicle.state
            planner_time_delta = 0.5
            self.local_path = []
            self.vehicle.path_time_delta = planner_time_delta
            self.vehicle.path = []

            while True:
                print("state", current_vehicle_state)
                print("goal", (current_node.x, current_node.y))
                planner = LocalPlanner(
                    current_vehicle_state,
                    (current_node.x, current_node.y),
                    planner_time_delta,
                    self.collision_detection,
                    self._display_surface
                )
                try:
                    path = planner.search()
                    if len(global_path) <= 0:
                        break
                    current_node = global_path.pop(0)
                    if len(path) < 1:
                        continue

                    self.vehicle.path += path[1:]
                    current_vehicle_state = path[-1]
                except Exception as e:
                    print(planner.steps_taken)
                    print(len(planner.queue))
                    print("Could not solve local planner path")
                    raise e

    def drive(self):
        while True:
            rotation = 0
            translation = 0
            xdelta = 0
            ydelta = 0
            for event in pygame.event.get():
                pressed_keys = pygame.key.get_pressed()
                if pressed_keys[pygame.K_a]:
                    rotation = pi * (1/16)
                elif pressed_keys[pygame.K_d]:
                    rotation = -pi * (1/16)
                
                if pressed_keys[pygame.K_w]:
                    translation = 0.25
                elif pressed_keys[pygame.K_s]:
                    translation = -0.25
                    
                thetadelta = rotation
                theta = self.vehicle.state.theta + thetadelta
                xdelta = translation*cos(theta)
                ydelta = translation*sin(theta)

            new_state = State(
                self.vehicle.state.x + xdelta,
                self.vehicle.state.y + ydelta,
                self.vehicle.state.theta + thetadelta
            )
            self.vehicle.state = new_state

            if self.collision_detection(self.vehicle):
                print("COLLISION!")

            self.render()
            pygame.display.update()
            self._frame_per_sec.tick(self._fps)


class CollisionMap(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()

        self.surf = pygame.image.load(COLLISION_MAP).convert_alpha()
        self.rect = self.surf.get_rect()
        self.rect.topleft= [0,0]
        self.mask = pygame.mask.from_surface(self.surf)