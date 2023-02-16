# -*- coding: utf-8 -*-


import arcade

from game import constants
from game.beings import Beings
from game.game import Game
from game.grid import Grid
from game.map_object import MapObject
from game.map_objects import MapObjects


grid = Grid()
map_object = MapObject(
    2,
    2,
    "image_map_object_city_1.png",
    destructible=True,
    target=True,
)
map_objects = MapObjects()
map_objects.add_map_object(map_object)

beings = Beings()

g = Game(
    constants.SCREEN_WIDTH,
    constants.SCREEN_HEIGHT,
    constants.SCREEN_TITLE,
    grid,
    beings,
)

g.beings.owner = g


if __name__ == "__main__":
    arcade.run()
