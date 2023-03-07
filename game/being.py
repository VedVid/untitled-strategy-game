# -*- coding: utf-8 -*-


# Using the Builder pattern.
# Source: https://github.com/faif/python-patterns/blob/master/patterns/creational/builder.py


from . import attacks
from . import constants
from .components.position import Position
from .components.sprite import Sprite


class Being:
    """
    Abstract class. Being can represent every animated entity, like player, allied units, monsters.
    """

    def __init__(self):
        self.build_cell_position(-1, -1)
        self.build_px_position(-1, -1)
        self.build_sprite()
        self.build_active_sprite()
        self.build_selected_sprite()
        self.build_targeted_sprite()
        self.build_hp()
        self.build_ai()
        self.build_active()

    def build_cell_position(self, x, y):
        raise NotImplementedError

    def build_px_position(self, x, y):
        raise NotImplementedError

    def build_sprite(self):
        raise NotImplementedError

    def build_active_sprite(self):
        raise NotImplementedError

    def build_selected_sprite(self):
        raise NotImplementedError

    def build_targeted_sprite(self):
        raise NotImplementedError

    def build_hp(self):
        raise NotImplementedError

    def build_attack(self):
        raise NotImplementedError

    def build_ai(self):
        raise NotImplementedError

    def build_active(self):
        self.active = False

    def toggle_active(self):
        if self.active:
            self.active = False
        else:
            self.active = True

    def move_to(self, x, y):
        raise NotImplementedError


# Concrete
class Player(Being):
    def build_cell_position(self, x, y):
        self.cell_position = Position(x, y)

    def build_px_position(self, x, y):
        # Position is redudant to sprite position...
        self.px_position = Position(
            (x * constants.TILE_SIZE_W) + constants.TILE_CENTER_OFFSET_X,
            (y * constants.TILE_SIZE_H) + constants.TILE_CENTER_OFFSET_Y,
        )

    def build_sprite(self):
        self.sprite = Sprite("image_being_player_1.png", self.px_position, 0.125)

    def build_active_sprite(self):
        self.sprite_active = Sprite(
            "image_being_player_1_active.png", self.px_position, 0.125
        )

    def build_selected_sprite(self):
        self.sprite_selected = Sprite(
            "image_being_player_1_selected.png", self.px_position, 0.125
        )

    def build_targeted_sprite(self):
        self.sprite_targeted = Sprite(
            "image_being_player_1_targeted.png", self.px_position, 0.125
        )

    def build_hp(self):
        self.hp = 3

    def build_attack(self):
        self.attack = attacks.attack_side_punch

    def build_ai(self):
        # If self.ai is None, then the instance will wait for the player's commands.
        self.ai = None

    def move_to(self, x, y):
        self.cell_position = Position(x, y)
        self.px_position = Position(
            (x * constants.TILE_SIZE_W) + constants.TILE_CENTER_OFFSET_X,
            (y * constants.TILE_SIZE_H) + constants.TILE_CENTER_OFFSET_Y,
        )
        self.sprite.update_position(self.px_position)
        self.sprite_active.update_position(self.px_position)
        self.sprite_selected.update_position(self.px_position)
        self.sprite_targeted.update_position(self.px_position)


# Concrete
class Enemy(Being):
    def build_cell_position(self, x, y):
        self.cell_position = Position(x, y)

    def build_px_position(self, x, y):
        self.px_position = Position(
            (x * constants.TILE_SIZE_W) + constants.TILE_CENTER_OFFSET_X,
            (y * constants.TILE_SIZE_H) + constants.TILE_CENTER_OFFSET_Y,
        )

    def build_sprite(self):
        self.sprite = Sprite("image_being_enemy_1.png", self.px_position, 0.125)

    def build_active_sprite(self):
        pass  # Does not have active_sprite

    def build_selected_sprite(self):
        self.sprite_selected = Sprite(
            "image_being_enemy_1_selected.png", self.px_position, 0.125
        )

    def build_targeted_sprite(self):
        self.sprite_targeted = Sprite(
            "image_being_enemy_1_targeted.png", self.px_position, 0.125
        )

    def build_hp(self):
        self.hp = 2

    def build_attack(self):
        self.attack = attacks.attack_punch

    def build_ai(self):
        # TODO: Replace this placeholder with proper AI.
        self.ai = None

    def move_to(self, x, y):
        self.cell_position = Position(x, y)
        self.px_position = Position(
            (x * constants.TILE_SIZE_W) + constants.TILE_CENTER_OFFSET_X,
            (y * constants.TILE_SIZE_H) + constants.TILE_CENTER_OFFSET_Y,
        )
        self.sprite.update_position(self.px_position)
        self.sprite_selected.update_position(self.px_position)
        self.sprite_targeted.update_position(self.px_position)


def construct_beings(cls, x, y):
    being = cls()
    being.build_cell_position(x, y)
    being.build_px_position(x, y)
    being.build_sprite()
    being.build_active_sprite()
    being.build_selected_sprite()
    being.build_targeted_sprite()
    being.build_attack()
    being.build_ai()
    being.build_active()
    return being
