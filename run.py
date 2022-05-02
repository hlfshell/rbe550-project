from delivery.state import State
from delivery.robot import Robot
from delivery.world import World

world = World()
world.set_vehicle(Robot(State(53.333, 20, 0)))
world.run()