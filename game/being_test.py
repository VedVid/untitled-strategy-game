# -*- coding: utf-8 -*-


from game import being
from game.components.sprite import Sprite
import game.constants as constants


being_player = being.construct_beings(being.Player, 2, 3)
being_enemy = being.construct_beings(being.Enemy, 5, 4)


def test_if_constants_remains_unchanged():
    """Change the values to match the current data."""
    assert (
        constants.TILE_SIZE_W == 64
        and constants.TILE_SIZE_H == 64
        and constants.TILE_CENTER_OFFSET_X == 32
        and constants.TILE_CENTER_OFFSET_Y == 32
    )


def test_player_class():
    assert type(being_player) is being.Player


def test_enemy_class():
    assert type(being_enemy) is being.Enemy


def test_player_ai():
    assert being_player.ai is None


def test_enemy_ai():
    # TODO: Remember to update this test when the proper ai will be added.
    assert being_enemy.ai is None


def test_player_position():
    assert being_player.position.x == 160 and being_player.position.y == 224
    assert (
        being_player.position.x == being_player.sprite.position.x
        and being_player.position.y == being_player.sprite.position.y
    )


def test_enemy_position():
    assert being_enemy.position.x == 352 and being_enemy.position.y == 288
    assert (
        being_enemy.position.x == being_enemy.sprite.position.x
        and being_enemy.position.y == being_enemy.sprite.position.y
    )
