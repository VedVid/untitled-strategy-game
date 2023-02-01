# -*- coding: utf-8 -*-


import arcade


class MapObjects:
    """This class stores all instances of MapObject for the currently shown map."""

    def __init__(self, objects=None):
        self.sprite_list = arcade.SpriteList()
        self.objects = objects
        if self.objects is None:
            self.objects = []

    def add_map_object(self, map_obj):
        self.objects.append(map_obj)
        self.sprite_list.append(map_obj.sprite.arcade_sprite)
