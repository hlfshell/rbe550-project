from delivery.state import State
from delivery.vehicle import Vehicle
from delivery.world import World

world = World()
world.set_vehicle(Vehicle(State(53.333, 20, 0)))
# world.drive()
# world.test_global_planner()
world.test_local_planner()
# world.test_cars()