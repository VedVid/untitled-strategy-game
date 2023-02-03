# -*- coding: utf-8 -*-


import arcade

from game.grid import Grid


grid = Grid(5, 10, 15, 20)


def test_grid_coords():
    assert grid.position.x == 5 and grid.position.y == 10


def test_grid_sprite_list_type():
    assert type(grid.sprite_list) == arcade.SpriteList


def test_grid_tiles_amount():
    assert len(grid.tiles) == 300
