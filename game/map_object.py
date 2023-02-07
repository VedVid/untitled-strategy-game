# -*- coding: utf-8 -*-


from . import constants
from .components.position import Position
from .components.sprite import Sprite


class MapObject:
    """
    MapObject is used to create every kind of inaminate object on the map, except for the background terrain.
    For example, MapObject may be used to place a coal mine, castle or village. MapObject instances are
    aggregated in MapObjects.

    Parameters:
    -----------
    x, y: int
        Coordinates of the object, passed as a position of a cell, later transformed to pixel values inside
        Position intance.
    sprite: str
        Name of the graphics that will represent MapObject on the map.
    blocks: bool
        Does this object blocks movement?
    destructible: bool
        Is it possible to destroy this object?
    target: bool
        Will ai try to destroy this object?
    Predecessor: MapObject
         Object that will replace this object if destroyed; None means object will be removed from the map
         and not replaced by another MapObject.

    Methods:
    --------
    destroy: MapObject
        Right now it is a placeholder method. It will remove MapObject from the MapObject, or replace
        current MapObject with its predecessor.
    """

    def __init__(
        self,
        x,  # For spawning MapObject, x and y coords refers to the cell position
        y,  # on the grid. During initialization it is converted to pixels.
        sprite,
        blocks=True,
        destructible=False,
        target=False,
        predecessor=None,
    ):
        self.cell_position = Position(x, y)
        self.px_position = Position(
            (x * constants.TILE_SIZE_W) + constants.TILE_CENTER_OFFSET_X,
            (y * constants.TILE_SIZE_H) + constants.TILE_CENTER_OFFSET_Y,
        )
        self.sprite = Sprite(sprite, self.px_position, 0.125)
        self.blocks = blocks
        self.destructible = destructible
        self.target = target
        self.predecessor = predecessor

    def destroy(self):
        """Returns predecessor after the original MapObject is destroyed (e.g. village is replaced by
        burned village). The replacement part is going to be handled in a different place
        (TODO: update loop, most likely).
        This method only returns the MapObject that will take place of this object."""
        if self.destructible:
            return self.predecessor
