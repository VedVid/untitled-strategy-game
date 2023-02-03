# -*- coding: utf-8 -*-


from game.components.sprite import Sprite
import game.constants as constants
from game.tile import Tile


tile = Tile(2, 4, "test.png")


def test_if_constants_remains_unchanged():
    """Change the values to match the current data."""
    assert (
        constants.TILE_SIZE_W == 64
        and constants.TILE_SIZE_H == 64
        and constants.TILE_CENTER_OFFSET_X == 32
        and constants.TILE_CENTER_OFFSET_Y == 32
    )


def test_tile_position():
    assert tile.position.x == 160 and tile.position.y == 288


def test_tile_sprite_type():
    assert type(tile.sprite) is Sprite
