# -*- coding: utf-8 -*-


from game import being


class TestBeing:
    being_player = being.construct_beings(being.Player, 2, 3)
    being_enemy = being.construct_beings(being.Enemy, 5, 4)

    def test_player_class(self):
        assert type(self.being_player) is being.Player

    def test_enemy_class(self):
        assert type(self.being_enemy) is being.Enemy

    def test_player_ai(self):
        assert self.being_player.ai is None

    def test_enemy_ai(self):
        # TODO: Remember to update this test when the proper ai will be added.
        assert self.being_enemy.ai is None

    def test_player_cell_position(self):
        assert (
            self.being_player.cell_position.x == 2
            and self.being_player.cell_position.y == 3
        )

    def test_player_px_position(self):
        assert (
            self.being_player.px_position.x == 160
            and self.being_player.px_position.y == 224
        )

    def test_player_sprite_position(self):
        assert (
            self.being_player.px_position.x == self.being_player.sprite.position.x
            and self.being_player.px_position.y == self.being_player.sprite.position.y
        )

    def test_enemy_cell_position(self):
        assert (
            self.being_enemy.cell_position.x == 5
            and self.being_enemy.cell_position.y == 4
        )

    def test_enemy_px_position(self):
        assert (
            self.being_enemy.px_position.x == 352
            and self.being_enemy.px_position.y == 288
        )

    def test_enemy_sprite_position(self):
        assert (
            self.being_enemy.px_position.x == self.being_enemy.sprite.position.x
            and self.being_enemy.px_position.y == self.being_enemy.sprite.position.y
        )


def test_being_move_to():
    being_player = being.construct_beings(being.Player, 2, 3)
    being_player.move_to(3, 3)
    assert being_player.cell_position.x == 3 and being_player.cell_position.y == 3
    assert being_player.px_position.x == 224 and being_player.px_position.y == 224
    assert (
        being_player.px_position.x
        == being_player.sprite.position.x
        == being_player.sprite_selected.position.x
        == being_player.sprite_targeted.position.x
    )
    assert (
        being_player.px_position.y
        == being_player.sprite.position.y
        == being_player.sprite_selected.position.y
        == being_player.sprite_targeted.position.y
    )
