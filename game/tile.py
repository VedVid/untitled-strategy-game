# -*- coding: utf-8 -*-


from . import constants

from game.components.size import Size
from game.components.position import Position
from game.components.sprite import Sprite


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
        self.position = Position(
            (x * constants.TILE_SIZE_W) + constants.TILE_CENTER_OFFSET_X,
            (y * constants.TILE_SIZE_H) + constants.TILE_CENTER_OFFSET_Y,
        )
        self.size = Size(width, height)
        self.sprite = Sprite(sprite, self.position, 0.125)
