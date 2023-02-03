# -*- coding: utf-8 -*-


from game.components.position import Position


def test_move_towards():
    tposition = Position(100, 100)
    tposition.move_towards(20, 40)
    assert tposition.x == 120 and tposition.y == 140
