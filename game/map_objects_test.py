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


map_object_center = MapObject(0, 0, "test.png")  # 4, 4 at the end of the test.
map_object_left = MapObject(3, 4, "test.png")
map_object_right = MapObject(5, 4, "test.png")
map_object_above = MapObject(4, 5, "test.png")
map_object_below = MapObject(4, 3, "test.png")


def test_for_empty_tiles_1():
    map_objects = MapObjects()
    map_objects.objects.append(map_object_center)
    assert len(map_objects._has_access_to_empty_tile(map_object_center)) == 2


def test_for_empty_tiles_2():
    map_object_center.cell_position.x = 4
    map_objects = MapObjects()
    map_objects.objects.append(map_object_center)
    assert len(map_objects._has_access_to_empty_tile(map_object_center)) == 3


def test_for_empty_tiles_3():
    map_object_center.cell_position.y = 4
    map_objects = MapObjects(
        [
            map_object_center,
            map_object_left,
            map_object_right,
            map_object_above,
            map_object_below,
        ]
    )
    assert len(map_objects._has_access_to_empty_tile(map_object_center)) == 0


def test_for_empty_tiles_4():
    map_object_below.blocks = False
    map_objects = MapObjects(
        [
            map_object_center,
            map_object_left,
            map_object_right,
            map_object_above,
            map_object_below,
        ]
    )
    assert len(map_objects._has_access_to_empty_tile(map_object_center)) == 1
