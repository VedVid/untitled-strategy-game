# -*- coding: utf-8 -*-


from . import constants

import game.components.size
import game.components.position


class Tile:
    """Class Tile have two components, Position and Size. Tiles are used to specify map grid."""
    def __init__(self, x, y, width=constants.GRID_SIZE_W, height=constants.GRID_SIZE_H):
        self.position = game.components.position.Position(x, y)
        self.size = game.components.size.Size(width, height)
