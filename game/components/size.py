# -*- coding: utf-8 -*-


class Size:
    """
    Component used to store the size (width, height) of the objects, especially sprites.

    Parameters:
    -----------
    width, height: int
        Width and height of Sprite or another instance owner.
    """

    def __init__(self, width, height):
        self.width = width
        self.height = height
