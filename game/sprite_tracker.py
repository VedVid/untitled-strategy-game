# -*- coding: utf-8 -*-


# At first, it was using facade pattern.
# Source: https://github.com/faif/python-patterns/blob/master/patterns/structural/facade.py
# but it lead to major code duplication.


import arcade

from . import globals
from .being import Player, Enemy
from .components.position import Position
from .map_object import MapObject
from .pathfinding import Pathfinder
from .states import State
from .tile import Tile


class SpriteTracker:
    """
    An actual facade that is going to track and draw all selected entities. Selected entity may be a selected player,
    targeted enemy, terrain sprite that is part of the path selected by pathfinding algorithm.
    Currently tracks Beings only.
    """

    def __init__(self, beings, grid):
        self._beings = beings
        self._grid = grid
        self._pathfinder = Pathfinder(grid)
        self._beings_sprites_selected = arcade.SpriteList()
        self._map_objects_sprites_selected = arcade.SpriteList()
        self._tiles_sprites_selected = arcade.SpriteList()
        self.mouse_position = None
        self.player = None

    def _reset_sprite_list_tiles(self):
        self._tiles_sprites_selected.clear()

    def _add_to_spritelist(self, entity, targeted=False):
        sprite = entity.sprite_selected.arcade_sprite
        if targeted:
            sprite = entity.sprite_targeted.arcade_sprite
        if isinstance(entity, Player) or isinstance(entity, Enemy):
            self._beings_sprites_selected.append(
                sprite
            )
        elif isinstance(entity, MapObject):
            self._map_objects_sprites_selected.append(
                sprite
            )
        elif isinstance(entity, Tile):
            self._tiles_sprites_selected.append(
                sprite
            )

    def _find(self, what):
        if what == "player_beings":
            l = self._beings.player_beings
        elif what == "enemy_beings":
            l = self._beings.enemy_beings
        elif what == "map_objects":
            l = self._grid.map_objects.objects
        elif what == "tiles":
            l = self._grid.tiles
        for effect in self.player.attack.effects:
            for coords in effect.target_positions:
                try:
                    pos = Position(
                        self.player.cell_position.x + coords[0],
                        self.player.cell_position.y + coords[1],
                    )
                    for e in l:
                        # Find "yellow" entity - ie tile that player can click on.
                        if (
                                e.cell_position.x == pos.x
                                and e.cell_position.y == pos.y
                        ):
                            self._add_to_spritelist(e)
                        # Find "red" entity - ie tile that will be attacked when player clicks on yellow tile.
                        if pos.x == self.mouse_position.x and pos.y == self.mouse_position.y:
                            for coords2 in effect.attack_pattern:
                                pos2 = Position(
                                    pos.x + coords2[0],
                                    pos.y + coords2[1],
                                )
                                if (
                                        e.cell_position.x == pos2.x
                                        and e.cell_position.y == pos2.y
                                ):
                                    self._add_to_spritelist(e, True)
                except AttributeError:
                    pass  # No valid player_being found.
                except ValueError as e:
                    print(f"{e} in sprite_tracker._find({what})")

    def _find_player_beings(self):
        for player in self._beings.player_beings:
            if player.active:
                self._beings_sprites_selected.append(player.sprite_active.arcade_sprite)
        if globals.state == State.TARGET:
            self._find("player_beings")

    def _find_enemy_beings(self):
        if globals.state == State.TARGET:
            self._find("enemy_beings")

    def _find_map_objects(self):
        if globals.state == State.TARGET:
            self._find("map_objects")

    def _find_tiles(self):
        if globals.state == State.MOVE:
            try:
                for coords in self._pathfinder.last_path:
                    tile = self._grid.find_tile_by_position(
                        Position(coords[0], coords[1])
                    )
                    self._tiles_sprites_selected.append(tile.sprite_path.arcade_sprite)
            except TypeError:  # Empty last_path
                pass
        elif globals.state == State.TARGET:
            self._find("tiles")

    def track(self, mouse_position, player=None):
        self._tiles_selected.find(mouse_position, player)
        self._map_objects_selected.find(mouse_position, player)
        self._beings_selected.find(mouse_position, player)

    def draw(self):
        self._tiles_selected.draw()
        self._map_objects_selected.draw()
        self._beings_selected.draw()


class BeingsSelected:
    def __init__(self, owner):
        self.owner = owner
        self.sprites_selected = arcade.SpriteList()

    def find(self, mouse_position, player=None):
        self._reset_sprite_list()
        self._find_player_beings_selected(mouse_position, player)
        self._find_enemy_beings_selected(mouse_position, player)

    def draw(self):
        self.sprites_selected.draw()


class MapObjectSelected:
    def __init__(self, owner):
        self.owner = owner
        self.sprites_selected = arcade.SpriteList()

    def _reset_sprite_list(self):
        self.sprites_selected.clear()


    def find(self, mouse_position, player=None):
        self._reset_sprite_list()
        self._find_map_objects_selected(mouse_position, player)

    def draw(self):
        self.sprites_selected.draw()


class TilesSelected:
    def __init__(self, grid):
        self.grid = grid
        self.pathfinder = Pathfinder(grid)
        self.sprites_selected = arcade.SpriteList()


    def find(self, mouse_position, player=None):
        self._reset_sprite_list()
        self._find_tiles_selected(mouse_position, player)

    def draw(self):
        self.sprites_selected.draw()
