# -*- coding: utf-8 -*-


import arcade

import game.components.position
import game.map_objects

from . import constants, drunkards_walk, tile


class Grid:
    """Grid represents the game map, and consists of Tiles. Attributes 'width' and 'height' represent
    number of columns and rows, not the pixel-wise dimensions."""

    def __init__(
        self,
        x=constants.TILE_CENTER_OFFSET_X,
        y=constants.TILE_CENTER_OFFSET_Y,
        width=constants.GRID_SIZE_W,
        height=constants.GRID_SIZE_H,
        map_objects=None,
    ):
        self.position = game.components.position.Position(x, y)
        self.width = width
        self.height = height
        self.sprite_list = arcade.SpriteList()
        self.tiles = self._init_empty_grid()
        self.map_objects = map_objects
        if self.map_objects is None:
            self.map_objects = game.map_objects.MapObjects()
            self.map_objects.owner = self

    def _init_empty_grid(self):
        """Initializes empty map, using the most basic terrain tile."""
        tiles = []
        for y in range(self.height):
            for x in range(self.width):
                new_tile = tile.Tile(
                    x,
                    y,
                    "image_terrain_1.png",
                )
                tiles.append(new_tile)
                self.sprite_list.append(new_tile.sprite.arcade_sprite)
        return tiles

    def generate_map(self):
        self.map_objects.fill_map()
        walker = drunkards_walk.DrunkardsWalk(owner=self, start_x=0, start_y=0)
        walker.walk()
