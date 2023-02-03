# -*- coding: utf-8 -*-


from . import constants
from game.components.position import Position
from game.components.sprite import Sprite


class MapObject:
    """Map object is, for example, a coal mine, castle, village.
    blocks: blocks movement?
    destructible: can be removed from the map?
    target: will ai try to destroy this object?
    predecessor: object that will replace this object if destroyed;
        None means object will be removed from the map and not replaced by another MapObject."""

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
        self.position = Position(
            (x * constants.TILE_SIZE_W) + constants.TILE_CENTER_OFFSET_X,
            (y * constants.TILE_SIZE_H) + constants.TILE_CENTER_OFFSET_Y,
        )
        self.sprite = Sprite(sprite, self.position, 0.125)
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
