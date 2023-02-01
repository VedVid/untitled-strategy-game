# -*- coding: utf-8 -*-


import game.components.position
import game.components.sprite


class MapObject:
    """Map object is, for example, a coal mine, castle, village.
    x, y: column and cell on map grid;
    blocks: blocks movement?
    destructible: can be removed from the map?
    target: will ai try to destroy this object?
    predecessor: object that will replace this object if destroyed;
        None means object will be removed from the map and not replaced by another MapObject."""

    def __init__(
        self,
        x,
        y,
        sprite,
        blocks=True,
        destructible=False,
        target=False,
        predecessor=None,
    ):
        self.position = game.components.position.Position(x, y)
        self.sprite = game.components.sprite.Sprite(sprite, self.position, 0.125)
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
