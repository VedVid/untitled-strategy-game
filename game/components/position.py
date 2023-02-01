# -*- coding: utf-8 -*-


class Position:
    """Component Position is used to place and move the owner on the screen."""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move_towards(self, dx, dy):
        self.x += dx
        self.y += dy
