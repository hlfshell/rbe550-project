from math import cos, pi, sin
import pygame
from delivery.map import Map
from delivery.state import State

from delivery.vehicle import Vehicle


BG_SPRITE = "./delivery/img/map.png" 
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

        self.goal = None

        self.vehicle: Vehicle = None
        self.map = Map.Get_Map()

        self._display_surface = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption("RBE550 Delivery Robot Project")

        self.bg_sprite: pygame.Surface = pygame.image.load(BG_SPRITE).convert_alpha()
        self.bg_sprite = pygame.transform.scale(self.bg_sprite, WINDOW_SIZE)

        self.render()
    
    def render(self):
        # Draw background color
        pygame.Surface.fill(self._display_surface, (0, 0, 0))
        self._display_surface.blit(self.bg_sprite, self.bg_sprite.get_rect())

        self.map.render(self._display_surface)

        if self.vehicle is not None:
            self.vehicle.render()
            self.vehicle.blit(self._display_surface)

    def set_vehicle(self, vehicle: Vehicle):
        self.vehicle = vehicle

    def collision_detection(self, vehicle) -> bool:
        pass
    
    def tick(self):
        pass

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

            self.collision_detection(self.vehicle)

            self.render()
            pygame.display.update()
            self._frame_per_sec.tick(self._fps)