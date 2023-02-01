# -*- coding: utf-8 -*-


import arcade

import game.constants
import game.map_object
import game.map_objects
import game.game
import game.grid


grid = game.grid.Grid()
test_map_object = game.map_object.MapObject(
    2,
    2,
    "image_map_object_city_1.png",
    destructible=True,
    target=True,
)
test_map_objects = game.map_objects.MapObjects()
test_map_objects.add_map_object(test_map_object)

g = game.game.Game(
    game.constants.SCREEN_WIDTH,
    game.constants.SCREEN_HEIGHT,
    game.constants.SCREEN_TITLE,
    grid,
    test_map_objects,
)


if __name__ == "__main__":
    print(len(g.grid.grid_sprite_list))
    arcade.run()
