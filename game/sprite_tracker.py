# -*- coding: utf-8 -*-


# At first, it was using facade pattern.
# Source: https://github.com/faif/python-patterns/blob/master/patterns/structural/facade.py
# but it lead to major code duplication, hence refactoring SpriteTracker to single class.


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
    _tiles_sprites_selected: arcade.SpriteList()
    _map_objects_sprites_selected: arcade.SpriteList()
    _beings_sprites_selected: arcade.SpriteList()
        Every _..._sprites_selected are SpriteLists that aggregate highlighted sprites: sprite_active, sprite_selected,
        sprite_targeted.
    mouse_position: Position
        Current Position of mouse, used to determine if cursor is over one of the currently shown sprite_selected, ergo
        to determine if sprite_targeted should be visible. mouse_position should be updated before every SpriteTracker
        usage.
    player: Being
        Currently active player; this value is used to determine a wide range of behaviours, from showing path to
        showing sprite_targeted.
    """

    def __init__(self, beings, grid):
        self._beings = beings
        self._grid = grid
        self._pathfinder = Pathfinder(grid)
        self._tiles_sprites_selected = arcade.SpriteList()
        self._map_objects_sprites_selected = arcade.SpriteList()
        self._beings_sprites_selected = arcade.SpriteList()
        self.mouse_position = None
        self.player = None

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
                            self._add_to_spritelist(entity)
                        # Find "red" entity - ie tile that will be attacked when player clicks on yellow tile.
                        if pos.x == self.mouse_position.x and pos.y == self.mouse_position.y:
                            for coords2 in effect.attack_pattern:
                                pos2 = Position(
                                    pos.x + coords2[0],
                                    pos.y + coords2[1],
                                )
                                if (
                                        entity.cell_position.x == pos2.x
                                        and entity.cell_position.y == pos2.y
                                ):
                                    self._add_to_spritelist(entity, True)
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

    def _reset_sprite_lists(self):
        self._beings_sprites_selected.clear()
        self._map_objects_sprites_selected.clear()
        self._tiles_sprites_selected.clear()

    def track(self):
        self._reset_sprite_lists()
        self._find_tiles()
        self._find_map_objects()
        self._find_enemy_beings()
        self._find_player_beings()

    def draw(self):
        self._tiles_sprites_selected.draw()
        self._map_objects_sprites_selected.draw()
        self._beings_sprites_selected.draw()
