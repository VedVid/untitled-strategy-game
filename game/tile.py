# -*- coding: utf-8 -*-


from . import constants

import game.components.size
import game.components.sprite
import game.components.position


class Tile:
    """Class Tile have three components: Position, Size, and Sprite. Sprite should be a path to the sprite, that
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
        self.sprite = game.components.sprite.Sprite(sprite, self.position, 0.125)
