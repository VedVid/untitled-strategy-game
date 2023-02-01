# -*- coding: utf-8 -*-


import arcade


class Game(arcade.Window):
    """Main game class."""

    def __init__(self, width, height, title, grid):
        super().__init__(width, height, title)
        self.background_color = arcade.color.DARK_BLUE_GRAY
        self.grid = grid

    def on_draw(self):
        self.clear()
        self.grid.grid_sprite_list.draw()
