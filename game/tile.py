# -*- coding: utf-8 -*-


from . import constants
from .components.size import Size
from .components.position import Position
from .components.sprite import Sprite


class Tile:
    """
    Instances of Tile are mostly used to represent terrain on Grid's cells.

    Parameters:
    -----------
    x, y: int
        Coords of cell which will be represented by the Tile; during instancing, cell coords are transformed Position
        instance with pixel values.
    sprite: string
        Name of the graphics that will represent Tile on the map.
    sprite_selected: string
        Name of the graphics that will be drawn over the basic sprite, if Tile is part of the currently showed path.
    width, height: int
        Size of the tile, converted to the instance of Size class.
    """

    def __init__(
        self,
        x,
        y,
        sprite=None,
        sprite_selected=None,
        width=constants.TILE_SIZE_W,
        height=constants.TILE_SIZE_H,
    ):
        self.cell_position = Position(x, y)
        self.px_position = Position(
            (x * constants.TILE_SIZE_W) + constants.TILE_CENTER_OFFSET_X,
            (y * constants.TILE_SIZE_H) + constants.TILE_CENTER_OFFSET_Y,
        )
        self.size = Size(width, height)
        self.sprite = Sprite(sprite, self.px_position, 0.125)
        if sprite_selected is None:
            sprite_selected = sprite
        self.sprite_selected = Sprite(sprite_selected, self.px_position, 0.125)
