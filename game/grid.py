# -*- coding: utf-8 -*-


import arcade

from . import constants
from .drunkards_walk import DrunkardsWalk
from .tile import Tile
from game.components.position import Position
from game.map_objects import MapObjects


class Grid:
    """
    Grid represents the game map, and consists of Tiles. While itself it only represents the terrain tiles,
    it also handles MapObjects and DrunkardsWalk to generate a map.

    Parameters:
    -----------
    x, y: int
        Where the grid is placed on the arcade.Window. By default, it starts from the bottom-left corner. Arcade Sprites
        coords refer to the center of sprite by default, hence TILE_CENTER_OFFSET as a default value to the parameter.
        x and y parameters are transformed into Position instance.
    width, height: int
        Dimensions of map, in cells.
    map_objects: MapObjects
        Instance of MapObjects (aggregator of MapObject instances; every inanimate object on map is MapObject).
        If not provided during creation of Grid, the basic MapObjects instance will be created instead, and map will
        be filled with mountains.

    Methods:
    --------
    _init_empty_grid: list of Tile
        Initializes empty grid, using one basic Sprite, creating the foundations for further modifications.
    generate_map
        Creates new DrunkardsWalk instance and lets him walk.
    """

    def __init__(
        self,
        x=constants.TILE_CENTER_OFFSET_X,
        y=constants.TILE_CENTER_OFFSET_Y,
        width=constants.GRID_SIZE_W,
        height=constants.GRID_SIZE_H,
        map_objects=None,
    ):
        self.position = Position(x, y)
        self.width = width
        self.height = height
        self.sprite_list = arcade.SpriteList()
        self.tiles = self._init_empty_grid()
        self.map_objects = map_objects
        if self.map_objects is None:
            self.map_objects = MapObjects()
            self.map_objects.owner = self
            self.map_objects.fill_map()

    def _init_empty_grid(self):
        """Initializes empty map, using the most basic terrain tile."""
        tiles = []
        for y in range(self.height):
            for x in range(self.width):
                tile = Tile(
                    x,
                    y,
                    "image_terrain_1.png",
                )
                tiles.append(tile)
                self.sprite_list.append(tile.sprite.arcade_sprite)
        return tiles

    def generate_map(self):
        walker = DrunkardsWalk(owner=self, start_x=0, start_y=0)
        walker.walk()
