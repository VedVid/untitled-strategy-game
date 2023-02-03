# -*- coding: utf-8 -*-


from game.components.sprite import Sprite
import game.constants as constants
from game.map_object import MapObject


map_object = MapObject(4, 2, "test.png")


def test_if_constants_remains_unchanged():
    """Change the values to match the current data."""
    assert (
        constants.TILE_SIZE_W == 64
        and constants.TILE_SIZE_H == 64
        and constants.TILE_CENTER_OFFSET_X == 32
        and constants.TILE_CENTER_OFFSET_Y == 32
    )


def test_map_object_position():
    assert map_object.position.x == 288 and map_object.position.y == 160


def test_map_object_sprite_type():
    assert type(map_object.sprite) is Sprite
