# -*- coding: utf-8 -*-


import arcade

from . import constants

import game.components.size
import game.components.position


class Tile:
    """Class Tile have three components: Position, Size, and sprite. Sprite should be a path to the sprite, that
    during the instancing is loaded as arcade.Sprite.
    Tiles are used to specify map grid."""

    def __init__(
        self,
        x,
        y,
        sprite=None,
        width=constants.TILE_SIZE_W,
        height=constants.TILE_SIZE_H,
    ):
        self.position = game.components.position.Position(x, y)
        self.size = game.components.size.Size(width, height)
        self.sprite = None
        if sprite:
            self.sprite = self.load_sprite(sprite)

    def load_sprite(self, sprite):
        """Tries to create an Arcade Sprite using specific graphic."""
        path = constants.DATA_PATH + sprite
        try:
            arcade_sprite = arcade.sprite.Sprite(path, scale=0.125)
            arcade_sprite.center_x = self.position.x + constants.TILE_CENTER_OFFSET_X
            arcade_sprite.center_y = self.position.y + constants.TILE_CENTER_OFFSET_Y
        except FileNotFoundError as e:
            print(e)
        else:
            return arcade_sprite
