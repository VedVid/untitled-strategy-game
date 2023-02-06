# -*- coding: utf-8 -*-


import arcade

from . import globals
from .states import State


class Game(arcade.Window):
    """Main game class."""

    def __init__(
        self,
        width,
        height,
        title,
        grid,
    ):
        super().__init__(width, height, title)
        self.background_color = arcade.color.DARK_BLUE_GRAY
        self.grid = grid
        # first_frame and initialized are hacks to allow removing from the spritelists.
        # Will be removed when stuff like main menu will be implemented - that way, window will be spawned and
        # GPU resources allocated long time before removing sprites.
        self.first_frame = True
        self.initialized = False

    def on_draw(self):
        self.clear()
        self.grid.sprite_list.draw()
        self.grid.map_objects.sprite_list.draw()
        if self.first_frame:
            self.first_frame = False
            self.initialized = True

    def on_update(self, delta_time):
        if globals.state == State.GENERATE_MAP and self.initialized:
            self.grid.generate_map()
            globals.state = State.PLAY
