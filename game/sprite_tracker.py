# -*- coding: utf-8 -*-


# Using facade pattern.
# Source: https://github.com/faif/python-patterns/blob/master/patterns/structural/facade.py


import arcade

from . import globals
from .components.position import Position
from .pathfinding import Pathfinder
from .states import State


class SpriteTracker:
    """
    An actual facade that is going to track and draw all selected entities. Selected entity may be a selected player,
    targeted enemy, terrain sprite that is part of the path selected by pathfinding algorithm.
    Currently tracks Beings only.
    """

    def __init__(self, beings, grid):
        self._map_objects_selected = MapObjectSelected(grid)
        self._beings_selected = BeingsSelected(beings)
        self._tiles_selected = TilesSelected(grid)

    def track(self, player=None):
        self._tiles_selected.find(player)
        self._map_objects_selected.find(player)
        self._beings_selected.find(player)

    def draw(self):
        self._tiles_selected.draw()
        self._map_objects_selected.draw()
        self._beings_selected.draw()


class BeingsSelected:
    def __init__(self, owner):
        self.owner = owner
        self.sprites_selected = arcade.SpriteList()

    def _reset_sprite_list(self):
        self.sprites_selected.clear()

    def _find_player_beings_selected(self, player=None):
        for player_ in self.owner.player_beings:
            if player_.selected:
                self.sprites_selected.append(player_.sprite_selected.arcade_sprite)
        if globals.state == State.TARGET:
            try:
                for effect in player.attack.effects:
                    for coords in effect.target_positions:
                        pos = Position(
                            player.cell_position.x + coords[0],
                            player.cell_position.y + coords[1],
                        )
                        for player_ in self.owner.player_beings:
                            if (
                                player_.cell_position.x == pos.x
                                and player_.cell_position.y == pos.y
                            ):
                                self.sprites_selected.append(
                                    player_.sprite_targeted.arcade_sprite
                                )
                                break
            except AttributeError:
                pass  # Catch-all
            except TypeError:
                pass  # Catch-all

    def _find_enemy_beings_selected(self, player=None):
        for enemy in self.owner.enemy_beings:
            if enemy.selected:
                self.sprites_selected.append(enemy.sprite_selected.arcade_sprite)
        if globals.state == State.TARGET:
            try:
                for effect in player.attack.effects:
                    for coords in effect.target_positions:
                        pos = Position(
                            player.cell_position.x + coords[0],
                            player.cell_position.y + coords[1],
                        )
                        for enemy in self.owner.enemy_beings:
                            if (
                                enemy.cell_position.x == pos.x
                                and enemy.cell_position.y == pos.y
                            ):
                                self.sprites_selected.append(
                                    enemy.sprite_targeted.arcade_sprite
                                )
                                break
            except AttributeError:
                pass  # Catch-all
            except TypeError:
                pass  # Catch-all

    def find(self, player=None):
        self._reset_sprite_list()
        self._find_player_beings_selected(player)
        self._find_enemy_beings_selected(player)

    def draw(self):
        self.sprites_selected.draw()


class MapObjectSelected:
    def __init__(self, owner):
        self.owner = owner
        self.sprites_selected = arcade.SpriteList()

    def _reset_sprite_list(self):
        self.sprites_selected.clear()

    def _find_map_objects_selected(self, player=None):
        if globals.state == State.TARGET:
            try:
                for effect in player.attack.effects:
                    for coords in effect.target_positions:
                        pos = Position(
                            player.cell_position.x + coords[0],
                            player.cell_position.y + coords[1],
                        )
                        for map_object in self.owner.map_objects.objects:
                            if (
                                map_object.cell_position.x == pos.x
                                and map_object.cell_position.y == pos.y
                            ):
                                self.sprites_selected.append(
                                    map_object.sprite_selected.arcade_sprite
                                )
                                break
            except AttributeError:
                pass  # Catch-all
            except TypeError:
                pass  # Catch-all

    def find(self, player=None):
        self._reset_sprite_list()
        self._find_map_objects_selected(player)

    def draw(self):
        self.sprites_selected.draw()


class TilesSelected:
    def __init__(self, grid):
        self.grid = grid
        self.pathfinder = Pathfinder(grid)
        self.sprites_selected = arcade.SpriteList()

    def _reset_sprite_list(self):
        self.sprites_selected.clear()

    def _find_tiles_selected(self, player=None):
        if globals.state == State.MOVE:
            try:
                for coords in self.pathfinder.last_path:
                    tile = self.grid.find_tile_by_position(
                        Position(coords[0], coords[1])
                    )
                    self.sprites_selected.append(tile.sprite_selected.arcade_sprite)
            except TypeError:  # Empty last_path
                pass
        elif globals.state == State.TARGET:
            try:
                for effect in player.attack.effects:
                    for coords in effect.target_positions:
                        tile_pos = Position(
                            player.cell_position.x + coords[0],
                            player.cell_position.y + coords[1],
                        )
                        tile = self.grid.find_tile_by_position(tile_pos)
                        self.sprites_selected.append(tile.sprite_targeted.arcade_sprite)
            except AttributeError:
                pass  # Catch-all
            except TypeError:
                pass  # Catch-all

    def find(self, player=None):
        self._reset_sprite_list()
        self._find_tiles_selected(player)

    def draw(self):
        self.sprites_selected.draw()
