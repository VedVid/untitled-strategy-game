# -*- coding: utf-8 -*-


from game.components.position import Position


def test_return_px_to_cell():
    tposition = Position(100, 180)
    cell_position = tposition.return_px_to_cell()
    assert cell_position.x == 1 and cell_position.y == 2
