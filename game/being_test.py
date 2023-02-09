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


def test_player_cell_position():
    assert being_player.cell_position.x == 2 and being_player.cell_position.y == 3


def test_player_px_position():
    assert being_player.px_position.x == 160 and being_player.px_position.y == 224


def test_player_sprite_position():
    assert (
        being_player.px_position.x == being_player.sprite.position.x
        and being_player.px_position.y == being_player.sprite.position.y
    )


def test_enemy_cell_position():
    assert being_enemy.cell_position.x == 5 and being_enemy.cell_position.y == 4


def test_enemy_px_position():
    assert being_enemy.px_position.x == 352 and being_enemy.px_position.y == 288


def test_enemy_sprite_position():
    assert (
            being_enemy.px_position.x == being_enemy.sprite.position.x
            and being_enemy.px_position.y == being_enemy.sprite.position.y
    )
