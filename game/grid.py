# -*- coding: utf-8 -*-


import arcade

from . import constants
from .components.position import Position
from .drunkards_walk import DrunkardsWalk
from .tile import Tile
from .map_objects import MapObjects


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
    _initialize_map_objects
        Clears self.map_objects, then fills it with new instance of MapObjects.
    generate_map
        Creates new DrunkardsWalk instance and lets him walk.
    check_map: bool
        After the map is created by DrunkardsWalk, check_map is called to validate the map.
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

    def _initialize_map_objects(self):
        """
        Start with setting the map_objects to None, then fill it with the basic MapObjects.
        Used in generate_map method to clean up the map between recursions.
        """
        self.map_objects = None
        self.map_objects = MapObjects()
        self.map_objects.owner = self
        self.map_objects.fill_map()

    def generate_map(self):
        """
        Runs the drunkard's walk algorithm to generate a map. If the map is not valid (e.g. Tile placement is
        not uniform enough), then map_objects are reset and generate_map is recursively called again.
        """
        walker = DrunkardsWalk(owner=self, start_x=0, start_y=0)
        walker.walk()
        self.map_objects.add_buildings()
        if not self.check_map():
            self._initialize_map_objects()
            self.generate_map()

    def check_map(self):
        """
        Check of uniformity of objects removal. The map is divided into four quadrants. This method counts
        MapObject instances remaining on each quadrant, calcs the average, then checks if every quadrant is within
        the bounds (average - negative-tolerance, average + positive tolerance). Returns a bool.
        TODO: Check if this is overkill for a such small maps. Perhaps could be merged with drunkard's walk?
        TODO: Check the longest path from A to B, to avoid player to navigate through circles.
        """
        # Declare the quadrants.
        quadrant_1 = [0, self.width // 2 - 1, 0, self.height // 2 - 1]
        quadrant_2 = [self.width // 2, self.width - 1, 0, self.height // 2 - 1]
        quadrant_3 = [
            self.width // 2,
            self.width - 1,
            self.height // 2,
            self.height - 1,
        ]
        quadrant_4 = [0, self.width // 2 - 1, self.height // 2, self.height - 1]
        # Every quadrants have its own counter, and after iterating over all the Tiles in quadrant,
        # the counter is added to the `count` list.
        count = []
        total = 0
        quadrants = [
            quadrant_1,
            quadrant_2,
            quadrant_3,
            quadrant_4,
        ]
        for quadrant in quadrants:
            counter = 0
            for x in range(quadrant[0], quadrant[1], 1):
                for y in range(quadrant[2], quadrant[3], 1):
                    # For every Tile in the current quadrant, transform its coords from the cell to pixels...
                    xx = (x * constants.TILE_SIZE_W) + constants.TILE_CENTER_OFFSET_X
                    yy = (y * constants.TILE_SIZE_H) + constants.TILE_CENTER_OFFSET_Y
                    # ...and check if there is object on this Tile.
                    obj = next(
                        (
                            obj
                            for obj in self.map_objects.objects
                            if (obj.px_position.x == xx and obj.px_position.y == yy)
                        ),
                        None,
                    )
                    # If object is found, increment the quadrant's counter.
                    if obj:
                        counter += 1
            count.append(counter)
            total += counter
        # After iterating over all four quadrants, calculate the average percentage of occupied terrain.
        average = total / len(quadrants)
        percent = average / 100
        # Then, check if uniformity of MapObject placement is withing specified in constant.py bounds.
        acceptable_minimum = average - (
            percent * constants.DIG_PERCENT_QUADRANT_TOLERANCE_NEGATIVE
        )
        acceptable_maximum = average + (
            percent * constants.DIG_PERCENT_QUADRANT_TOLERANCE_POSITIVE
        )
        for c in count:
            if c < acceptable_minimum or c > acceptable_maximum:
                return False  # Invalid map
        return True  # Valid map
