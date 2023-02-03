# -*- coding: utf-8 -*-


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
    move_towards
        Changes position into direction specified by method arguments.
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move_towards(self, dx, dy):
        self.x += dx
        self.y += dy
