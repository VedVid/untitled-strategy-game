# -*- coding: utf-8 -*-


import arcade

import game.components.position

from . import constants, tile


class Grid:
    """Grid represents the game map, and consists of Tiles. Attributes 'width' and 'height' represent
    number of columns and rows, not the pixel-wise dimensions."""

    def __init__(
        self,
        x=constants.TILE_CENTER_OFFSET_X,
        y=constants.TILE_CENTER_OFFSET_Y,
        width=constants.GRID_SIZE_W,
        height=constants.GRID_SIZE_H,
    ):
        self.position = game.components.position.Position(x, y)
        self.width = width
        self.height = height
        self.grid_sprite_list = arcade.SpriteList()
        self.tiles = self._init_empty_grid()

    def _init_empty_grid(self):
        """Initializes empty map, using the most basic terrain tile."""
        tiles = []
        for y in range(self.height):
            for x in range(self.width):
                new_tile = tile.Tile(
                    self.position.x + x * constants.TILE_SIZE_W,
                    self.position.y + y * constants.TILE_SIZE_H,
                    "image_terrain_1.png",
                )
                tiles.append(new_tile)
                self.grid_sprite_list.append(new_tile.sprite)
        return tiles
