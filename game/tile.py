# -*- coding: utf-8 -*-


from . import constants

from game.components.size import Size
from game.components.position import Position
from game.components.sprite import Sprite


class Tile:
    """
    Instances of Tile are mostly used to represent terrain on Grid's cells.

    Parameters:
    -----------
    x, y: int
        Coords of cell which will be represented by the Tile; during instancing, cell coords are transformed Position
        instance with pixel values.
    sprite: string
        Name of the graphics that will represent MapObject on the map.
    width, height: int
        Size of the tile, converted to the instance of Size class.
    """

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
