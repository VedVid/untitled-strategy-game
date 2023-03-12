# -*- coding: utf-8 -*-


from game.components.sprite import Sprite
from game.map_object import MapObject


map_object = MapObject(4, 2, "test.png", "test_selected.png", "test_targeted.png")
successor = MapObject(
    6, 6, "test.png", "test_selected.png", "test_targeted.png", successor=None
)
map_object.successor = successor


def test_map_object_cell_position():
    assert map_object.cell_position.x == 4 and map_object.cell_position.y == 2


def test_map_object_px_position():
    assert map_object.px_position.x == 288 and map_object.px_position.y == 160


def test_map_object_sprite_type():
    assert type(map_object.sprite) is Sprite


def test_map_object_successor_binding():
    assert map_object.successor is successor


def test_map_object_destroy():
    new_map_object = map_object.destroy()
    assert new_map_object is successor
