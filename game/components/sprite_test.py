# -*- coding: utf-8 -*-


import arcade

from game.components.position import Position
from game.components.sprite import Sprite


sprite = Sprite("test.png", Position(0, 0), 0.125)


def test_valid_instance():
    assert (
        sprite.arcade_sprite.center_x == sprite.position.x
        and sprite.arcade_sprite.center_y == sprite.position.y
    )


def test_arcade_sprite_type():
    assert type(sprite.arcade_sprite) is arcade.sprite.Sprite
