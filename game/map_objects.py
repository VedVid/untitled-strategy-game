# -*- coding: utf-8 -*-


import copy
import random

import arcade

from . import constants
from .map_object import MapObject


class MapObjects:
    """
    This class stores all instances of MapObject for the currently shown map.

    Parameters:
    -----------
    objects: list of MapObject
        One can pass existing list of MapObject instances to MapObjects. By default, objects parameter is equal to None,
        and then the empty list is initialized.

    Methods:
    --------
    fill_map
        Using Grid width and height values, creates a baseic MapObject for every cell.

    add_buildings
        Adds buildings to the map.

    _has_access_to_empty_tile (MapObject): dict
        Checks if there are other MapObjects on the Tiles adjacent to the MapObject. Returns dict.

    replace_map_object (MapObject, MapObject)
        Replaces first MapObject with second MapObject.

    add_map_object (MapObject)
        Adds new MapObject to self.objects, and its sprite to arcade SpriteList.

    remove_map_object (MapObject)
        Removes a specific MapObject and its sprite from self.object and arcade SpriteList.
        Please note that the removal can not occur before window initialization (ergo, before allocation of
        GPU resources).
    """

    def __init__(self, objects=None):
        self.owner = None
        self.sprite_list = arcade.SpriteList()
        self.objects = objects
        if self.objects is None:
            self.objects = []

    def fill_map(self):
        """Called at the beginning of map generation, fills the map with mountains."""
        for y in range(self.owner.height):
            for x in range(self.owner.width):
                map_object = MapObject(
                    x,
                    y,
                    "image_map_object_mountain_1.png",
                    "image_map_object_mountain_1_selected.png",
                    "image_map_object_mountain_1_targeted.png",
                    successor=None,
                )
                self.add_map_object(map_object)

    def add_buildings(self):
        """
        Adds buildings to the map by replacing mountains by buildings. A valid place to spawn a building is
        an existing MapObject that has access to at least one empty Tile.
        """
        buildings_num = random.randint(
            constants.BUILDINGS_NUMBER_MIN,
            constants.BUILDINGS_NUMBER_MAX,
        )
        objects_ = copy.copy(self.objects)
        random.shuffle(objects_)
        while buildings_num > 0:
            try:
                obj = objects_.pop()
            except IndexError:
                break
            if self._has_access_to_empty_tile(obj):
                ruins = MapObject(
                    obj.cell_position.x,
                    obj.cell_position.y,
                    "image_map_object_ruins_1.png",
                    "image_map_object_ruins_1_selected.png",
                    "image_map_object_ruins_1_targeted.png",
                    blocks=True,
                    target=False,
                    successor=None,
                )
                city = MapObject(
                    ruins.cell_position.x,
                    ruins.cell_position.y,
                    "image_map_object_city_1.png",
                    "image_map_object_city_1_selected.png",
                    "image_map_object_city_1_targeted.png",
                    blocks=True,
                    target=True,
                    successor=ruins,
                )
                self.replace_map_object(obj, city)
                buildings_num -= 1

    def _has_access_to_empty_tile(self, map_object):
        """
        Checks if there are other MapObjects on the Tiles adjacent to the MapObject.
        Starts with dict filled with positions to check, then removes the dict keys if the position is occupied.
        TODO: Think about more elegant solution.
        """
        empty_tiles = {
            "left": (map_object.cell_position.x - 1, map_object.cell_position.y),
            "right": (map_object.cell_position.x + 1, map_object.cell_position.y),
            "above": (map_object.cell_position.x, map_object.cell_position.y + 1),
            "below": (map_object.cell_position.x, map_object.cell_position.y - 1),
        }
        # Check ends of the map, both horizontally...
        if map_object.cell_position.x == 0:
            del empty_tiles["left"]
        elif map_object.cell_position.x == constants.GRID_SIZE_W - 1:
            del empty_tiles["right"]
        # ...and vertically.
        if map_object.cell_position.y == 0:
            del empty_tiles["below"]
        elif map_object.cell_position.y == constants.GRID_SIZE_H - 1:
            del empty_tiles["above"]
        # Then check for the neighbour objects.
        for obj in self.objects:
            if obj is map_object or not obj.blocks:
                continue
            if obj.cell_position.x == map_object.cell_position.x:
                if obj.cell_position.y == map_object.cell_position.y - 1:
                    del empty_tiles["below"]
                elif obj.cell_position.y == map_object.cell_position.y + 1:
                    del empty_tiles["above"]
            else:
                if obj.cell_position.y == map_object.cell_position.y:
                    if obj.cell_position.x == map_object.cell_position.x - 1:
                        del empty_tiles["left"]
                    elif obj.cell_position.x == map_object.cell_position.x + 1:
                        del empty_tiles["right"]
        return empty_tiles

    def replace_map_object(self, old_map_object, new_map_object):
        self.remove_map_object(old_map_object)
        self.add_map_object(new_map_object)

    def add_map_object(self, map_object):
        self.objects.append(map_object)
        self.sprite_list.append(map_object.sprite.arcade_sprite)

    def remove_map_object(self, map_object):
        self.objects.remove(map_object)
        self.sprite_list.remove(map_object.sprite.arcade_sprite)

    def find_map_object_by_cell_position(self, x, y):
        """Tries to find MapObject instance based on cell position. Returns MapObject or None."""
        return next(
            (
                obj
                for obj in self.objects
                if (obj.cell_position.x == x and obj.cell_position.y == y)
            ),
            None,
        )

    def find_map_object_by_px_position(self, x, y):
        """
        Tries to find MapObject instance based on range of px_position, where px_position is the center of sprite.
        Returns MapObject or None.
        """
        min_x = x - (constants.TILE_SIZE_W / 2)
        max_x = x + (constants.TILE_SIZE_W / 2)
        min_y = y - (constants.TILE_SIZE_H / 2)
        max_y = y + (constants.TILE_SIZE_H / 2)
        return next(
            (
                obj
                for obj in self.objects
                if (
                    min_x <= obj.px_position.x <= max_x
                    and min_y <= obj.px_position.y <= max_y
                )
            ),
            None,
        )
