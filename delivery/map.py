from __future__ import annotations
from collections import defaultdict
from math import sqrt
from typing import Dict, List, Tuple

import pygame


class Node():

    def __init__(
        self,
        id: float,
        coords: Tuple[int, int],
        type: str,
        neighbors: List[int]
    ):
        self.id = id
        pixels_per_meter = 15
        self.x: float = coords[0] / pixels_per_meter
        self.y: float = coords[1] / pixels_per_meter
        self.type = type
        self.neighbors = neighbors
    
    def distance_between(self, other: Node) -> float:
        return sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

    @property
    def pixel_xy(self) -> Tuple[int, int]:
        pixels_per_meter = 15
        return round(self.x * pixels_per_meter), round(self.y * pixels_per_meter)
    
    @property
    def color(self) -> Tuple[int, int, int]:
        color = (0, 0, 0)
        if self.id == 6:
            color = (255, 0, 0)
        if self.type == "start":
            color = (0, 255, 0)
        elif self.type == "delivery":
            color = (0, 0, 255)
        return color
    
    def __eq__(self, other: Node) -> bool:
        if other is None:
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)
    
    def __lt__(self, other: Node) -> bool:
        if other is None:
            return False
        return self.id < other.id

    def __str__(self) -> str:
        return f"{self.id}:{self.type}:({self.x, self.y})"

class Map():

    def __init__(self):
        self.nodes: Dict[int, Node] = {}
        self.locks: defaultdict(lambda: []) = {}

    def toggle_robot_lock(self, node: int) -> bool:
        if len(self.locks[node]) == 0:
            self.locks[node] = ["robot"]
            return False
        elif len(self.locks[node]) > 1:
            return True
        elif self.locks[node] == "robot":
            self.locks[node] = []
            return False
        else:
            return True

    def toggle_car_lock(self, car_id: str, node: int) -> bool:
        if len(self.locks[node]) == 0:
            self.locks[node] = [car_id]
            return False
        elif self.locks[node][0] == "robot":
            return True
        elif car_id in self.locks[node]:
            self.locks[node].remove(car_id)
            return False
        else:
            self.locks[node].append(car_id)
            return False

    def add_node(self, node: Node):
        if node.id in self.nodes:
            raise Exception("Node already exists")
        self.nodes[node.id] = node

    def get_neighbors(self, node: Node) -> List[Node]:
        neighbors: List[Node] = []
        for neighbor_id in node.neighbors:
            neighbor = self.nodes[neighbor_id]
            neighbors.append(neighbor)
        return neighbors

    def nearest_node(self, x: float, y: float) -> int:
        nearest_node = 0
        closest_distance = 9999
        for node in self.nodes.values():
            distance = sqrt(
                (x - node.x)**2 +
                (y - node.y)**2
            )
            if distance < closest_distance:
                nearest_node = node.id
                closest_distance = distance
        return nearest_node

    @property
    def start(self) -> Node:
        return self.nodes[0]

    def render(self, surface: pygame.Surface):
        # First, draw each line between neighbors
        for id in self.nodes:
            node = self.nodes[id]
            xy = node.pixel_xy
            for neighbor in self.get_neighbors(node):
                pygame.draw.line(surface, (255, 0, 0), xy, neighbor.pixel_xy, 3)
        # Then draw the nodes. We do this to overlap connections
        # and not vice versa
        for id in self.nodes:
            node = self.nodes[id]
            pygame.draw.circle(surface, node.color, node.pixel_xy, 5)

    @staticmethod
    def _Create_Map_From_Nodes(nodes: List[Node]) -> Map:
        map = Map()
        for node in nodes:
            map.add_node(node)
        return map

    @staticmethod
    def Get_Map() -> Map:
        return Map._Create_Map_From_Nodes(_nodes)

_nodes=[
    Node(0, (800,300), 'start', [1]),
    Node(1, (655,300), 'waypoint', [0,2,21]),
    Node(2, (655,230), 'crosswalk', [1,3,4]),
    Node(3, (660,200), 'corner', [2,47]),
    Node(4, (525,230), 'crosswalk', [2,18,19]),
    Node(5, (270,230), 'crosswalk', [15,16,6]),
    Node(6, (140,230), 'crosswalk', [5,7]),
    Node(7, (140,300), 'delivery', [6,8]),
    Node(8, (140,580), 'corner', [7,9]),
    Node(9, (210,580), 'delivery', [8,10]),
    Node(10, (310,580), 'crosswalk', [9,11]),
    Node(11, (360,580), 'corner', [10,12]),
    Node(12, (360,770), 'corner', [11]),
    Node(13, (310,450), 'crosswalk', [10,14,18]),
    Node(14, (270,450), 'corner', [13,15]),
    Node(15, (270,320), 'delivery', [5,14]),
    Node(16, (270,170), 'delivery', [5,17]),
    Node(17, (270,20), 'delivery', [16]),
    Node(18, (525,450), 'corner', [4,13]),
    Node(19, (525,65), 'delivery', [4,20]),
    Node(20, (660,65), 'delivery', [19]),
    Node(21, (655,445), 'corner', [1,22]),
    Node(22, (690,445), 'crosswalk', [21,23]),
    Node(23, (690,580), 'crosswalk', [22,24,25]),
    Node(24, (600,580), 'delivery', [23]),
    Node(25, (750,585), 'corner', [23,26]),
    Node(26, (750,740), 'crosswalk', [25,27]),
    Node(27, (885,740), 'crosswalk', [26,28,29]),
    Node(28, (885,445), 'corner', [22,27]),
    Node(29, (885,770), 'corner', [27,30]),
    Node(30, (1275,770), 'delivery', [29,31]),
    Node(31, (1430,770), 'corner', [30,32]),
    Node(32, (1430,585), 'corner', [31,33]),
    Node(33, (1370,585), 'delivery', [32,34]),
    Node(34, (1210,580), 'corner', [33,35]),
    Node(35, (1205,485), 'delivery', [34,36]),
    Node(36, (1205,305), 'delivery', [37,35]),
    Node(37, (1205,235), 'crosswalk', [36,38,39]),
    Node(38, (1205,200), 'corner', [47,37]),
    Node(39, (1335,235), 'crosswalk', [37,42,40]),
    Node(40, (1335,165), 'delivery', [39,41]),
    Node(41, (1335,25), 'delivery', [40]),
    Node(42, (1335,325), 'delivery', [39,43]),
    Node(43, (1340,445), 'corner', [42,44]),
    Node(44, (1370,445), 'crosswalk', [33,43,48]),
    Node(45, (1590,445), 'corner', [48,46]),
    Node(46, (1590,65), 'delivery', [45]),
    Node(47, (885,200), 'delivery', [3,38]),
    Node(48, (1450,445), 'delivery', [45,44])
]