# -*- coding: utf-8 -*-


from game.map_object import MapObject
from game.map_objects import MapObjects


fake_map_object = MapObject(1, 1, "test.png")
map_objects_filled = MapObjects([fake_map_object])
map_objects_empty = MapObjects(None)


def test_map_objects_filled():
    assert len(map_objects_filled.objects) > 0


def test_map_objects_filled_remove():
    map_objects_filled.objects.remove(fake_map_object)
    assert len(map_objects_filled.objects) == 0


def test_map_objects_empty_type():
    assert type(map_objects_empty.objects) is list


def test_map_objects_empty_length():
    assert len(map_objects_empty.objects) == 0


def test_map_objects_empty_add():
    map_objects_empty.objects.append(fake_map_object)
    assert len(map_objects_empty.objects) == 1
