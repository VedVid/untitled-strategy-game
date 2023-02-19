# -*- coding: utf-8 -*-


from game.components.position import Position
from game.grid import Grid
from game.map_object import MapObject
from game.map_objects import MapObjects
from game.pathfinding import Pathfinder


def test_moving_around_the_obstacle():
    map_objects = MapObjects()
    map_object = MapObject(2, 2, "test.png", blocks=True)
    map_objects.add_map_object(map_object)
    grid = Grid(width=5, height=5, map_objects=map_objects)
    position_1 = Position(1, 2)
    position_2 = Position(3, 2)
    pathfinder = Pathfinder(grid)
    path_1, _ = pathfinder.find_path(position_1, position_2)
    print(pathfinder._path_grid.grid_str(path=path_1, start=position_1, end=position_2))
    position_3 = Position(0, 2)
    position_4 = Position(4, 2)
    pathfinder.clean_up_path_grid()
    path_2, _ = pathfinder.find_path(position_3, position_4)
    print(pathfinder._path_grid.grid_str(path=path_2, start=position_3, end=position_4))
    assert len(path_1) == 5 and len(path_2) == 7
