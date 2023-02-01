# -*- coding: utf-8 -*-


import arcade

from .. import constants


class Sprite:
    """Sprite class holds all the data necessary to create an arcade.Sprite instance, ie:
    path-to-the-graphic, sprite position, and prite scale."""

    def __init__(self, filename, position, scale=1):
        self.filename = filename
        self.position = position
        self.scale = scale
        self.arcade_sprite = self._load()

    def _load(self):
        """Tries to create an Arcade Sprite using specific graphic."""
        path = constants.DATA_PATH + self.filename
        try:
            arcade_sprite = arcade.sprite.Sprite(path, self.scale)
            arcade_sprite.center_x = self.position.x + constants.TILE_CENTER_OFFSET_X
            arcade_sprite.center_y = self.position.y + constants.TILE_CENTER_OFFSET_Y
        except FileNotFoundError as e:
            print(e)
        else:
            return arcade_sprite
