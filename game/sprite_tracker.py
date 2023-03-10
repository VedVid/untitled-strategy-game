# -*- coding: utf-8 -*-


# At first, it was using facade pattern.
# Source: https://github.com/faif/python-patterns/blob/master/patterns/structural/facade.py
# but it lead to major code duplication, hence refactoring SpriteTracker to single class.


import math

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
    SpriteTracker tracks all sprites that should be highlighted: active player, path from player to cursor,
    targets, etc. Before every use of SpriteTracker, 'player' and 'mouse_position' should be updated.
    sprite_active is currently selected player, sprite_selected (should be renamed maybe?) are sprites that player
    can click on (like when choosing a tile to attack from 4 available), sprite_targeted are sprites that will be
    affected by attack (shown only when cursor is over sprite_selected).

    Attributes:
    -----------
    _beings: Beings
        Takes instance of Beings; used to highlight active player, and players and enemies in the area of attack.
    _grid: Grid
        Takes instance of Grid; used to highlight targeted MapObject and Tile instances.
    _pathfinder: Pathfinder
        New instance of monostate-like Pathfinder class; used to hightlight path from active player to cursor.
    _tiles_sprites_in_range: arcade.SpriteList()
    _tiles_sprites_selected: arcade.SpriteList()
    _map_objects_sprites_selected: arcade.SpriteList()
    _beings_sprites_selected: arcade.SpriteList()
        Every _..._sprites_selected are SpriteLists that aggregate highlighted sprites: sprite_in_range, sprite_active,
        sprite_selected, sprite_targeted.
    mouse_position: Position
        Current Position of mouse, used to determine if cursor is over one of the currently shown sprite_selected, ergo
        to determine if sprite_targeted should be visible. mouse_position should be updated before every SpriteTracker
        usage.
    player: Being
        Currently active player; this value is used to determine a wide range of behaviours, from showing path to
        showing sprite_targeted.

    Methods:
    --------
    _add_to_sprite_list (Tile | MapObject | Player | Enemy, bool=False)
        Takes entity as first argument and bool for a second argument. Based on the entity type, the game adds sprites
        to the correct arcarde.SpriteList. Boolean value is used to decide if sprite_selected (default)
        or sprite_targeted should be used.
    _find (string)
        Generic-as-possible method to find all sprite_selected and sprite_targeted to show. String passed as argument
        is used to determine what list (from: tiles, map_objects, beings) will be iterated over to find the sprites.
        Uses string as argument because passing lists as arguments in Python results in unpredictable behaviour.
    _find_player_beings
    _find_enemy_beings
    _find_map_objects
    _find_tiles
        All these methods at the beginning handle additional cases that depend on the entity type, then call _find.
    _reset_sprite_lists
        Clears _tiles_sprites_selected, _map_objects_sprites_selected, and _beings_sprites_selected.
    track
        One of two public methods of SpriteTracker. 'track' clears all SpriteLists then fills them again by calling
        _find_... methods.
    draw
        Draws every Sprites that should be highlighted.
    """

    def __init__(self, beings, grid):
        self._beings = beings
        self._grid = grid
        self._pathfinder = Pathfinder(grid)
        self._tiles_sprites_in_range = arcade.SpriteList()
        self._tiles_sprites_selected = arcade.SpriteList()
        self._map_objects_sprites_selected = arcade.SpriteList()
        self._beings_sprites_selected = arcade.SpriteList()
        self.mouse_position = None
        self.player = None

    def _add_to_sprite_list(self, entity, targeted=False):
        """
        Adds entity sprite to corresponding sprite_list.
        Defaults to sprite_selected, but may add sprite_targeted too.
        """
        sprite = entity.sprite_selected.arcade_sprite
        if targeted:
            sprite = entity.sprite_targeted.arcade_sprite
        if isinstance(entity, Player) or isinstance(entity, Enemy):
            self._beings_sprites_selected.append(sprite)
        elif isinstance(entity, MapObject):
            self._map_objects_sprites_selected.append(sprite)
        elif isinstance(entity, Tile):
            self._tiles_sprites_selected.append(sprite)

    def _find(self, what):
        """
        Generic method used to find and add Sprites to _..._sprites_selected. Finds both "yellow" Sprites
        (sprite_selected, so sprites that are highlighted when player enters targeting mode) and "red" Sprites
        (sprite_targeted, when player hovers mouse over sprite_selected).
        Assigns lists using string passed as argument, because directly passing lists as argument may result in
        unpredicatble behaviour.
        """
        l = None
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
                    for entity in l:
                        # Find "yellow" entity - ie tile that player can click on.
                        if (
                            entity.cell_position.x == pos.x
                            and entity.cell_position.y == pos.y
                        ):
                            self._add_to_sprite_list(entity)
                        # Find "red" entity - ie tile that will be attacked when player clicks on yellow tile.
                        if (
                            pos.x == self.mouse_position.x
                            and pos.y == self.mouse_position.y
                        ):
                            for coords2 in effect.attack_pattern:
                                pos2 = Position(
                                    pos.x + coords2[0],
                                    pos.y + coords2[1],
                                )
                                if (
                                    entity.cell_position.x == pos2.x
                                    and entity.cell_position.y == pos2.y
                                ):
                                    self._add_to_sprite_list(entity, True)
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
            # Draw all tiles that are in player range.
            for tile in self._grid.tiles:
                self._pathfinder.set_up_path_grid(self._beings)
                self._pathfinder.find_path(
                    self.player.cell_position,
                    tile.cell_position,
                )
                for i, coords in enumerate(self._pathfinder.last_path):
                    tile = self._grid.find_tile_by_position(
                        Position(coords[0], coords[1])
                    )
                    try:
                        if i <= self.player.range:
                            self._tiles_sprites_in_range.append(tile.sprite_in_range.arcade_sprite)
                    except ValueError as e:  # Sprite already in SpriteList. .clear() not called?
                        pass
            try:
                # Then show path from player to cursor.
                self._pathfinder.set_up_path_grid(self._beings)
                self._pathfinder.find_path(
                    self.player.cell_position,
                    self.mouse_position,
                )
                for i, coords in enumerate(self._pathfinder.last_path):
                    tile = self._grid.find_tile_by_position(
                        Position(coords[0], coords[1])
                    )
                    # Use green "sprite_path" if tile is in range of active player.
                    spr = tile.sprite_path
                    if i > self.player.range:
                        # Otherwise, use red "sprite_targeted".
                        spr = tile.sprite_targeted
                    self._tiles_sprites_selected.append(spr.arcade_sprite)
            except TypeError:  # Empty last_path
                pass
        elif globals.state == State.TARGET:
            self._find("tiles")

    def _reset_sprite_lists(self):
        self._beings_sprites_selected.clear()
        self._map_objects_sprites_selected.clear()
        self._tiles_sprites_in_range.clear()
        self._tiles_sprites_selected.clear()

    def track(self):
        """Clears all arcade.SpriteList instances in SpriteTracker and fills them again with updated data."""
        self._reset_sprite_lists()
        self._find_tiles()
        self._find_map_objects()
        self._find_enemy_beings()
        self._find_player_beings()

    def draw(self):
        self._tiles_sprites_in_range.draw()
        self._tiles_sprites_selected.draw()
        self._map_objects_sprites_selected.draw()
        self._beings_sprites_selected.draw()
