# -*- coding: utf-8 -*-


from .. import constants


class Position:
    """
    Component used to place and move the owner on the screen.

    Parameters:
    -----------
    x, y: int
        Position on the map. Uses pixel values to accurately place the owner on the screen. However, during
        being created during instancing of Tile or MapObject, passed parameters are based on the cell position often.

    Methods:
    --------
    return_px_to_cell: Position(int, int)
        Returns new Position. Assumes that the coords of the current Position instance are in pixels, and converts them
        to the cells.
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def return_px_to_cell(self):
        """
        Returns new position, with coords converted from the px coords of the current instance of Position to the
        cell position.
        """
        # TODO: When we convert cell position to px position, then we multiply x, y by tile size, then we add the
        # TODO  offset. Yet currently, looks like when we convert from px to cell, taking into account offset leads to
        # TODO  the wrong results. Observed first time when tinkering with Game.on_mouse_movement.
        cell_x = self.x // constants.TILE_SIZE_W
        cell_y = self.y // constants.TILE_SIZE_H
        return Position(int(cell_x), int(cell_y))
