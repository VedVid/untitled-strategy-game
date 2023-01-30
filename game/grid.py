# -*- coding: utf-8 -*-


from . import tile


class Grid:
    """Grid represents the game map, and consists of Tiles. Attributes 'width' and 'height' represent
    number of columns and rows, not the pixel-wise dimensions."""
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self._init_empty_grid()

    def _init_empty_grid(self):
        tiles = []
        for y in range(self.height):
            for x in range(self.width):
                new_tile = tile.Tile(x, y)
                tiles.append(new_tile)
        return tiles
