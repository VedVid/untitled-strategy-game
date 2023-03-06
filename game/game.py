# -*- coding: utf-8 -*-


import arcade

from . import constants
from . import globals
from .components.position import Position
from .pathfinding import Pathfinder
from .sprite_tracker import SpriteTracker
from .states import State


class Game(arcade.Window):
    """Main game class."""

    def __init__(
        self,
        width,
        height,
        title,
        grid,
        beings,
    ):
        super().__init__(width, height, title)
        self.x = 0
        self.y = 0
        self.background_color = arcade.color.DARK_BLUE_GRAY
        self.grid = grid
        self.beings = beings
        self.pathfinder = Pathfinder(self.grid)
        self.selected_player = None
        self.sprite_tracker = SpriteTracker(self.beings, self.grid)
        # first_frame and initialized are hacks to allow removing from the spritelists.
        # Will be removed when stuff like main menu will be implemented - that way, window will be spawned and
        # GPU resources allocated long time before removing sprites.
        self.first_frame = True
        self.initialized = False

    def on_draw(self):
        self.clear()
        self.grid.sprite_list.draw()
        self.grid.map_objects.sprite_list.draw()
        self.beings.player_sprite_list.draw()
        self.beings.enemy_sprite_list.draw()
        self.sprite_tracker.draw()
        if self.first_frame:
            self.first_frame = False
            self.initialized = True

    def on_key_press(self, key, modifiers):
        # TODO: TESTING ONLY, remove later!
        if key == arcade.key.ENTER:
            if globals.state == State.MOVE:
                globals.state = State.TARGET
            else:
                globals.state = State.MOVE

    def on_mouse_motion(self, x, y, dx, dy):
        self.x = x
        self.y = y
        if self.selected_player:
            target_position = Position(x, y).return_px_to_cell()
            self.pathfinder.set_up_path_grid(self.beings)
            self.pathfinder.find_path(
                self.selected_player.cell_position, target_position
            )

    def on_mouse_press(self, x, y, button, modifiers):
        player_under_cursor = self.beings.find_player_by_px_position(x, y)
        if button == arcade.MOUSE_BUTTON_LEFT:
            if player_under_cursor:
                for player in self.beings.player_beings:
                    if player is player_under_cursor:
                        globals.state = State.MOVE
                        player.toggle_selected()
                        continue
                    player.selected = False
                return
            if self.selected_player is not None:
                if self.pathfinder.last_path and globals.state == State.MOVE:
                    self.selected_player.move_to(
                        self.pathfinder.last_path[-1][0],
                        self.pathfinder.last_path[-1][1],
                    )
                    self.pathfinder.last_path = ()
                elif globals.state == State.TARGET:
                    try:
                        self.selected_player.attack.perform(self.beings, x, y)
                    except TypeError:
                        pass  # Catch-all exception for attacks.
        elif button == arcade.MOUSE_BUTTON_RIGHT:
            if globals.state == State.TARGET:
                globals.state = State.MOVE
            elif globals.state == State.MOVE:
                globals.state = State.PLAY
                self.selected_player.selected = False
                self.selected_player = None

    def on_update(self, delta_time):
        if globals.state == State.GENERATE_MAP and self.initialized:
            self.grid.generate_map()
            globals.state = State.PLAY
            for i in range(constants.PLAYER_BEINGS_NO):
                self.beings.spawn_player_being()
            for i in range(constants.ENEMY_BEINGS_INITIAL_NO):
                self.beings.spawn_enemy_being()
        if self.initialized:
            self.selected_player = self.beings.find_selected_player()
            if self.selected_player is None:
                globals.state = State.PLAY
                self.pathfinder.last_path = ()
            elif globals.state == State.PLAY:
                globals.state = State.MOVE
            self.sprite_tracker.track(self.selected_player)
            # TODO: TESTING ONLY, REMOVE LATER!
            for enemy in self.beings.enemy_beings:
                if enemy.hp <= 0:
                    self.beings.remove_enemy_being(enemy)
