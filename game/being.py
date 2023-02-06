# -*- coding: utf-8 -*-


# Using the Builder pattern.
# Source: https://github.com/faif/python-patterns/blob/master/patterns/creational/builder.py


from . import constants
from .components.position import Position
from .components.sprite import Sprite


class Being:
    """
    Abstract class. Being can represent every animated entity, like player, allied units, monsters.
    """
    def __init__(self):
        self.build_position(-1, -1)
        self.build_sprite()
        self.build_ai()

    def build_position(self, x, y):
        raise NotImplementedError

    def build_sprite(self):
        raise NotImplementedError

    def build_ai(self):
        raise NotImplementedError


# Concrete
class Player(Being):
    def build_position(self, x, y):
        # Position is redudant to sprite position... Unless we keep this position in cell units instead of pixel.
        self.position = Position(
            (x * constants.TILE_SIZE_W) + constants.TILE_CENTER_OFFSET_X,
            (y * constants.TILE_SIZE_H) + constants.TILE_CENTER_OFFSET_Y,
        )

    def build_sprite(self):
        self.sprite = Sprite("image_being_player_1.png", self.position, 0.125)

    def build_ai(self):
        # If self.ai is None, then the instance will wait for the player's commands.
        self.ai = None


# Concrete
class Enemy(Being):
    def build_position(self, x, y):
        self.position = Position(
            (x * constants.TILE_SIZE_W) + constants.TILE_CENTER_OFFSET_X,
            (y * constants.TILE_SIZE_H) + constants.TILE_CENTER_OFFSET_Y,
        )

    def build_sprite(self):
        self.sprite = Sprite("image_being_enemy_1.png", self.position, 0.125)

    def build_ai(self):
        # TODO: Replace this placeholder with proper AI.
        self.ai = None


def construct_beings(cls, x, y):
    being = cls()
    being.build_position(x, y)
    being.build_sprite()
    being.build_ai()
    return being
