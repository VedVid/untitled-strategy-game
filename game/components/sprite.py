# -*- coding: utf-8 -*-


import arcade

from .. import constants


class Sprite:
    """
    Sprite class holds all the data necessary to create an arcade.Sprite instance, ie:
    path-to-the-graphic, sprite position, and sprite scale.

    Parameters:
    -----------
    filename: str
        Name if file, without path (that is taken from constants.py), with extension.
    position: Position
        Instance of Position class, contains x and y coordinates.
    scale: int or float
        Makes Sprite larger or smaller.

    Methods:
    --------
    _load
        Creates Arcade Sprite using parameters passed during the initialization.
    update_position (Position)
        Updates position of self and arcade_sprite.
    """

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
            arcade_sprite.center_x = self.position.x
            arcade_sprite.center_y = self.position.y
        except FileNotFoundError as e:
            print(e)
        else:
            return arcade_sprite

    def update_position(self, position):
        """Updates position of Sprite that is already set up."""
        self.position = position
        self.arcade_sprite.center_x = self.position.x
        self.arcade_sprite.center_y = self.position.y
