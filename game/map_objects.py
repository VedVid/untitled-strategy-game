# -*- coding: utf-8 -*-


import arcade

from game.map_object import MapObject


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

    add_map_object
        Adds new MapObject to self.objects, and its sprite to arcade SpriteList

    remove_map_object
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
        for y in range(self.owner.height):
            for x in range(self.owner.width):
                map_object = MapObject(x, y, "image_map_object_mountain_1.png")
                self.add_map_object(map_object)

    def add_map_object(self, map_object):
        self.objects.append(map_object)
        self.sprite_list.append(map_object.sprite.arcade_sprite)

    def remove_map_object(self, map_object):
        self.objects.remove(map_object)
        self.sprite_list.remove(map_object.sprite.arcade_sprite)
