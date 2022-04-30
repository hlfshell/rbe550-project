from math import cos, pi, sin
from multiprocessing import RLock
from random import choice
from threading import Thread
from time import perf_counter, time
from typing import List
from uuid import uuid4
import pygame
from queue import Queue
from delivery.car import Car, CarPaths
from delivery.global_planner import GlobalPlanner
from delivery.local_planner import LocalPlanner
from delivery.map import Map, Node
from delivery.obstacle import Obstacle
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

        self.last_tick: float = 0.0

        self.vehicle: Vehicle = None
        self.map = Map.Get_Map()

        self.goal: int = None
        self.global_path: List[Node] = None
        self.local_path: List[State] = None
        self.future_local_paths: List[List[State]] = []

        self.path_lock = RLock()
        self.path_id: str = None
        self.planning: bool = False

        self._display_surface = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption("RBE550 Delivery Robot Project")

        self.bg_sprite: pygame.Surface = pygame.image.load(BG_SPRITE).convert_alpha()
        self.bg_sprite = pygame.transform.scale(self.bg_sprite, WINDOW_SIZE)

        self._collision_map: pygame.sprite.Group = pygame.sprite.Group()
        self._collision_map.add(CollisionMap())

        self.obstacles: List[Obstacle] = Obstacle.Load_Obstacles()

        self.cars: List[Car] = []

        self.render()
    
    def render(self):
        # Draw background color
        pygame.Surface.fill(self._display_surface, (0, 0, 0))
        self._display_surface.blit(self.bg_sprite, self.bg_sprite.get_rect())

        self.map.render(self._display_surface)
        self.draw_global_path()
        self.draw_local_paths()

        for obstacle in self.obstacles:
            obstacle.render(self._display_surface)

        if self.vehicle is not None:
            self.vehicle.render()
            self.vehicle.blit(self._display_surface)

        for car in self.cars:
            car.render()
            car.blit(self._display_surface)

    def tick(self):
        # Normally a time tick should be every 1/60 (1/fps), but if it's
        # slower this makes the appropriate adjustment
        if self.last_tick == 0.0:
            time_delta = 1/self._fps
        else:
            time_delta = perf_counter() - self.last_tick

        for car in self.cars:
            if car.path_finished==True:
                path = car.path
                self.cars.remove(car)
                self.cars.append(Car(path))
            else:
                car.tick(time_delta)

 #       with self.path_lock:
 #           # Determine where the car is on its path.
 #           index = self.vehicle.global_path_step
 #           if len(self.future_local_paths) >= index + 1 and \
 #               self.vehicle.path is None:
 #                   self.vehicle.path = self.future_local_paths[index] #[1:]

 #       self.vehicle.tick(time_delta)

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
    
    def draw_local_paths(self):
        with self.path_lock:
            paths = self.future_local_paths.copy()

        if len(paths) < 1:
            return
        
        # with self.path_lock:
        for path in paths:
            for state in path:
                self._display_surface.fill(
                    (0, 0, 255),
                    (state.pixel_xy,
                    (6,6))
                )

    def set_vehicle(self, vehicle: Vehicle):
        self.vehicle = vehicle

    def collision_detection(self, vehicle: Vehicle) -> bool:
        # Map collisions first
        off_map_collisions = pygame.sprite.spritecollide(
            vehicle,
            self._collision_map,
            False,
            pygame.sprite.collide_mask
        )
        if len(off_map_collisions) > 0:
            return True
        
        # Then obstacles
        for obstacle in self.obstacles:
            if obstacle.rect.colliderect(vehicle.rect):
                offset = (
                    vehicle.rect[0] - obstacle.rect[0],
                    vehicle.rect[1] - obstacle.rect[1]
                )
                collisions = obstacle.mask.overlap(vehicle.mask, offset)
                if collisions is not None and len(collisions) > 0:
                    return True

        return False

    def choose_goal(self):
        # Determine if we are near the grocery store or the delivery
        # target
        nearest_node = self.map.nearest_node(self.vehicle.state.x, self.vehicle.state.y)

        if nearest_node == 0:
            if self.goal == None:
                chosen_goal = choice(
                    [node for node in self.map.nodes.values() if node.type == "delivery"]
                )
                self.goal = chosen_goal.id
        else:
            self.goal = 0

    def global_plan(self):
        if self.goal is None:
            return

        goal = self.map.nodes[self.goal]
        
        nearest_id = self.map.nearest_node(self.vehicle.state.x, self.vehicle.state.y)
        nearest_node = self.map.nodes[nearest_id]
        planner = GlobalPlanner(self.map, nearest_node, goal)
        self.global_path = planner.search()

    def test_cars(self):
        for path in CarPaths:
            self.cars.append(Car(path))

        while True:
            self.tick()
            self.render()
            pygame.event.get()
            pygame.display.update()
            print(pygame.mouse.get_pos())
            self._frame_per_sec.tick(self._fps)

    def test_global_planner(self):
        time_start: float = 0.0
        while True:
            if time() - time_start >= 1.0:
                self.global_plan()
                time_start = time()
            self.render()
            pygame.event.get()

    def plan(self):
        # Determine first if we are at the end of our path. If so,
        # reset the path so that we can assign a new one.
        if self.global_path is not None and \
            self.vehicle.global_path_step == len(self.global_path):
            with self.path_lock:
                self.goal = None
                self.global_path = None
                self.future_local_paths = []
                self.vehicle.reset_goal()

        if self.goal is None:
            self.choose_goal()

        if self.global_path is None:
            # Generate a global path
            self.global_plan()

        with self.path_lock:
            id = self.path_id
        
        if id is not None:
            return
        
        with self.path_lock:
            # Check to see if we are actively planning
            if self.planning:
                return

            # If we don't have a global path, we can't continue
            if self.global_path is None or len(self.global_path) <= 0:
                return

            # Determine if we've already calculated the full path
            if len(self.future_local_paths) == len(self.global_path):
                return
            
            # OK, we need more local paths, and we are not actively
            # running a path planner right now
            # We are targeting the next node in the global path we have
            # not yet planned a path to. We know this by comparing
            # plan list lengths
            index = len(self.future_local_paths)
            goal = self.global_path[index]
            # The last state of the last local path is our start state
            # for this path
            if len(self.future_local_paths) <= 0:
                current_vehicle_state = self.vehicle.state
            else:
                current_vehicle_state = self.future_local_paths[-1][-1]
            planner = LocalPlanner(
                current_vehicle_state,
                (goal.x, goal.y),
                2.0,
                self.collision_detection,
                self._display_surface
            )
            # Finally, fire off the thread
            self.planning = True
            Thread(target=self._plan, args=[self.path_id, planner]).start()
 
    def _plan(self, path_id: str, planner: LocalPlanner):
        try:
            path = planner.search()

            if len(path) < 1:
                return
            
            with self.path_lock:
                # If the plan id has changed, we no longer need this path
                if self.path_id != path_id:
                    return

                # If the plan id matches, append this to the local paths,
                # minus the starting path since we're already there.
                if len(self.future_local_paths) > 0:
                    path = path[1:]
                self.future_local_paths.append(path)
        except Exception as e:
            print("Could not solve local planner path")
            raise e
        finally:
            with self.path_lock:
                self.planning = False

    def test_local_async_planner(self):
        while True:
            self.render()
            self.tick()
            self.plan()
            pygame.event.get()
            pygame.display.update()
            self._frame_per_sec.tick(self._fps)

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
            planner_time_delta = 2.0
            self.local_path = []
            self.vehicle.path_time_delta = planner_time_delta
            self.vehicle.path = []

            while True:
                print("state", current_vehicle_state)
                print("goal", (current_node.x, current_node.y))
                with self.path_lock:
                    with self.lock:
                        if self.local_path is not None:
                            continue
                        if self.path_id is None:
                            self.path_id = str(uuid4())

                        planner = LocalPlanner(
                            current_vehicle_state,
                            (current_node.x, current_node.y),
                            planner_time_delta,
                            self.collision_detection,
                            self._display_surface
                        )

                        Thread(target=self.plan, args=[self.path_id, planner])
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

                        self.future_local_paths.append(path)
                        current_vehicle_state = path[-1]
                    except Exception as e:
                        print(planner.steps_taken)
                        print(len(planner.queue))
                        print("Could not solve local planner path")
                        raise e

            # Now that we have the path, let's physically
            # move the robot over
            while self.vehicle.state != self.vehicle.path[-1]:
                self.tick()
                self.render()
                pygame.event.get()
                pygame.display.update()
                self._frame_per_sec.tick(self._fps)

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