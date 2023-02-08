# -*- coding: utf-8 -*-


from game.components.position import Position
from game.grid import Grid
from game.map_object import MapObject
from game.map_objects import MapObjects
from game.pathfinding import Pathfinder


def test_moving_around_the_obstacle():
    map_objects = MapObjects()
    map_object = MapObject(1, 1, "test.png", blocks=True)
    map_objects.add_map_object(map_object)
    grid = Grid(width=3, height=3, map_objects=map_objects)
    position_1 = Position(0, 1)
    position_2 = Position(2, 1)
    pathfinder = Pathfinder(grid)
    path, _ = pathfinder.find_path(position_1, position_2)
    print(pathfinder._path_grid.grid_str(path=path, start=position_1, end=position_2))
    assert len(path) == 5
