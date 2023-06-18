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
    sprite_path: string
        Name of the graphics that will be drawn from player to cursor to show path.
    sprite_in_range: string
        Name of the graphics that will be used to show what tiles are in range of active player.
    overlayed_by: list of Beings
        List of beings that are targeting this tile. If list is empty, then no overlay is drawn.
    width, height: int
        Size of the tile, converted to the instance of Size class.

    Methods:
    --------
    add_overlay (Being)
        Adds new reference to Being that targets this tile.
    remove_overlay (Being)
        Removes reference to Being that used to target this tile, but it does not do this anymore, because it died
        or moved.
    """

    def __init__(
        self,
        x,
        y,
        sprite=None,
        sprite_selected=None,
        sprite_targeted=None,
        sprite_path=None,
        sprite_in_range=None,
        overlayed_by=None,
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
        if sprite_targeted is None:
            sprite_targeted = sprite
        self.sprite_targeted = Sprite(sprite_targeted, self.px_position, 0.125)
        if sprite_path is None:
            sprite_path = sprite
        self.sprite_path = Sprite(sprite_path, self.px_position, 0.125)
        if sprite_in_range is None:
            sprite_in_range = sprite
        self.sprite_in_range = Sprite(sprite_in_range, self.px_position, 0.125)
        self.sprite_overlayed = Sprite("target.png", self.px_position, 0.125)
        self.overlayed_by = overlayed_by
        if self.overlayed_by is None:
            self.overlayed_by = []

    def add_overlay(self, being):
        self.overlayed_by.append(being)

    def remove_overlay(self, being):
        self.overlayed_by.remove(being)
