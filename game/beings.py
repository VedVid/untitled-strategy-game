# -*- coding: utf-8 -*-


import random

import arcade

from . import being
from . import constants


class Beings:
    """
    This class stores all instances of Being currently shown.

    Parameters:
    -----------
    player_beings: list of Beings
        List of player-controlled Beings.
        One can pass existing list of Being instances to Beings. By default, objects parameter is equal to None,
        and then the empty list is initialized.
    enemy_beings: list of Beings
        List of Beings that represent enemies.
        One can pass existing list of Being instances to Beings. By default, objects parameter is equal to None,
        and then the empty list is initialized.

    Methods:
    --------
    find_being_by_cell_position (int, int): Being
        Finds and returns any Being instance found on the specific coordinates. Arguments indicate the column and row
        of the game map.

    find_player_by_px_position (int, int): Being
        Finds and returns any Being instance found on the specific coordinates. Arguments indicate the center position
        of the sprite on the screen, using pixels.

    spawn_player_being (int, int)
        Tries to spawn player at the coordinates. If -1 is passed as argument, then game choices the coordinate
        randomly.

    add_player_being (Being)
        Adds new player-controlled Being to self.player_beings, and its sprite to arcade SpriteList.

    remove_player_being (Being)
        Removes a player-controlled Being and its sprite from self.player_beings and arcade SpriteList.
        Please note that the removal can not occur before window initialization (ergo, before allocation of
        GPU resources).

    find_enemy_by_px_position (int, int): Being
        Finds and returns any Being instance found on the specific coordinates. Arguments indicate the center position
        of the sprite on the screen, using pixels.

    spawn_enemy_being (int, int)
        Works exactly the same way as spawn_player_being method, but for enemies. When the amount of Being types will
        grow, then (TODO) these two methods should be merged; player / enemy should be passed by argument.

    add_enemy_being (Being)
        Adds new enemy Being to self.enemy_beings, and its sprite to arcade SpriteList.

    remove_enemy_being (Being)
        Removes an enemy Being and its sprite from self.enemy_beings and arcade SpriteList.
        Please note that the removal can not occur before window initialization (ergo, before allocation of
        GPU resources).
    """

    def __init__(self, player_beings=None, enemy_beings=None):
        self.owner = None
        self.player_sprite_list = arcade.SpriteList()
        self.player_beings = []
        # TODO: Rewrite GameObjects like that.
        if player_beings is not None:
            for player in player_beings:
                self.add_player_being(player)
        self.enemy_sprite_list = arcade.SpriteList()
        self.enemy_beings = []
        if enemy_beings is not None:
            for enemy in enemy_beings:
                self.add_enemy_being(enemy)

    def find_selected_player(self):
        return next(
            (p for p in self.player_beings if (p.selected)),
            None,
        )

    def find_being_by_cell_position(self, x, y):
        """
        Check if there is any Being instance (no matter, friend or foe) at the specific coords.
        Uses cell_position attribute. Returns Being instance or None.
        """
        all_beings = self.player_beings + self.enemy_beings
        return next(
            (
                b
                for b in all_beings
                if (b.cell_position.x == x and b.cell_position.y == y)
            ),
            None,
        )

    def find_being_by_px_position(self, x, y):
        being_ = self.find_player_by_px_position(x, y)
        if being_ is None:
            being_ = self.find_enemy_by_px_position(x, y)
        return being_

    def find_player_by_px_position(self, x, y):
        """
        Check if there is any friendly Being instance at the specific coords.
        Uses px_position attribute. Returns Being instance or None.
        """
        min_x = x - (constants.TILE_SIZE_W / 2)
        max_x = x + (constants.TILE_SIZE_W / 2)
        min_y = y - (constants.TILE_SIZE_H / 2)
        max_y = y + (constants.TILE_SIZE_H / 2)
        return next(
            (
                b
                for b in self.player_beings
                if (
                    min_x <= b.px_position.x <= max_x
                    and min_y <= b.px_position.y <= max_y
                )
            ),
            None,
        )

    def spawn_player_being(self, x=-1, y=-1):
        """
        Tries to spawn player Being. This method let you to pass specific coordinates to spawn the player Being, but
        if the place is occupied by other Being or MapObject, then it tries to spawn player again on random coordinates.
        """
        if x < 0:
            x = random.randrange(0, constants.GRID_SIZE_W)
        if y < 0:
            y = random.randrange(0, constants.GRID_SIZE_H)
        o = self.owner.grid.map_objects.find_map_object_by_cell_position(x, y)
        b = self.find_being_by_cell_position(x, y)
        if o is not None or b is not None:
            self.spawn_player_being(-1, -1)
        else:
            player_being = being.construct_beings(being.Player, x, y)
            self.add_player_being(player_being)

    def add_player_being(self, player_being):
        self.player_beings.append(player_being)
        self.player_sprite_list.append(player_being.sprite.arcade_sprite)

    # TODO: Write a method to retrieve player_being (and map_object for that matter) by coords.
    def remove_player_being(self, player_being):
        self.player_beings.remove(player_being)
        self.player_sprite_list.remove(player_being.sprite.arcade_sprite)

    def find_enemy_by_px_position(self, x, y):
        """
        Check if there is any enemy Being instance at the specific coords.
        Uses px_position attribute. Returns Being instance or None.
        """
        min_x = x - (constants.TILE_SIZE_W / 2)
        max_x = x + (constants.TILE_SIZE_W / 2)
        min_y = y - (constants.TILE_SIZE_H / 2)
        max_y = y + (constants.TILE_SIZE_H / 2)
        return next(
            (
                b
                for b in self.enemy_beings
                if (
                    min_x <= b.px_position.x <= max_x
                    and min_y <= b.px_position.y <= max_y
                )
            ),
            None,
        )

    def spawn_enemy_being(self, x=-1, y=-1):
        """
        Tries to spawn enemy Being. This method let you to pass specific coordinates to spawn the enemy Being, but
        if the place is occupied by other Being or MapObject, then it tries to spawn enemy again on random coordinates.
        """
        if x < 0:
            x = random.randrange(0, constants.GRID_SIZE_W)
        if y < 0:
            y = random.randrange(0, constants.GRID_SIZE_H)
        o = self.owner.grid.map_objects.find_map_object_by_cell_position(x, y)
        b = self.find_being_by_cell_position(x, y)
        if o is not None or b is not None:
            self.spawn_enemy_being(-1, -1)
        else:
            enemy_being = being.construct_beings(being.Enemy, x, y)
            self.add_enemy_being(enemy_being)

    def add_enemy_being(self, enemy_being):
        self.enemy_beings.append(enemy_being)
        self.enemy_sprite_list.append(enemy_being.sprite.arcade_sprite)

    def remove_enemy_being(self, enemy_being):
        self.enemy_beings.remove(enemy_being)
        self.enemy_sprite_list.remove(enemy_being.sprite.arcade_sprite)
