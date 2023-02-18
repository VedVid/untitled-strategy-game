# -*- coding: utf-8 -*-


# Using facade pattern.
# Source: https://github.com/faif/python-patterns/blob/master/patterns/structural/facade.py


import arcade

from .components.position import Position
from .pathfinding import Pathfinder


class SpriteTracker:
    """
    An actual facade that is going to track and draw all selected entities. Selected entity may be a selected player,
    targeted enemy, terrain sprite that is part of the path selected by pathfinding algorithm.
    Currently tracks Beings only.
    """

    def __init__(self, beings, grid):
        self._beings_selected = BeingsSelected(beings)
        self._tiles_selected = TilesSelected(grid)

    def track(self):
        self._tiles_selected.find()
        self._beings_selected.find()

    def draw(self):
        self._tiles_selected.draw()
        self._beings_selected.draw()


class BeingsSelected:
    def __init__(self, owner):
        self.owner = owner
        self.sprites_selected = arcade.SpriteList()

    def _reset_sprite_list(self):
        self.sprites_selected.clear()

    def _find_player_beings_selected(self):
        for player in self.owner.player_beings:
            if player.selected:
                self.sprites_selected.append(player.sprite_selected.arcade_sprite)

    def _find_enemy_beings_selected(self):
        for enemy in self.owner.enemy_beings:
            if enemy.selected:
                self.sprites_selected.append(enemy.sprite_selected.arcade_sprite)

    def find(self):
        self._reset_sprite_list()
        self._find_player_beings_selected()
        self._find_enemy_beings_selected()

    def draw(self):
        self.sprites_selected.draw()


class MapObjectSelected:
    pass


class TilesSelected:
    def __init__(self, grid):
        self.grid = grid
        self.pathfinder = Pathfinder(grid)
        self.sprites_selected = arcade.SpriteList()

    def _reset_sprite_list(self):
        self.sprites_selected.clear()

    def _find_tiles_selected(self):
        try:
            for coords in self.pathfinder.last_path:
                tile = self.grid.find_tile_by_position(Position(coords[0], coords[1]))
                self.sprites_selected.append(tile.sprite_selected.arcade_sprite)
        except TypeError:  # Empty last_path
            pass

    def find(self):
        self._reset_sprite_list()
        self._find_tiles_selected()

    def draw(self):
        self.sprites_selected.draw()
