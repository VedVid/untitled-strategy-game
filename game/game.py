# -*- coding: utf-8 -*-


import arcade

from . import constants
from . import globals
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
        self.pathfinder = None
        self.sprite_tracker = SpriteTracker(self.beings)
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
        pass

    def on_mouse_motion(self, x, y, dx, dy):
        self.x = x
        self.y = y

    def on_mouse_press(self, x, y, button, modifiers):
        selected_player = self.beings.find_player_by_px_position(x, y)
        if selected_player:
            for player in self.beings.player_beings:
                if player is selected_player:
                    player.toggle_selected()
                    continue
                player.selected = False

    def on_update(self, delta_time):
        if globals.state == State.GENERATE_MAP and self.initialized:
            self.grid.generate_map()
            globals.state = State.PLAY
            for i in range(constants.PLAYER_BEINGS_NO):
                self.beings.spawn_player_being()
        if self.initialized:
            self.sprite_tracker.track()
