# -*- coding: utf-8 -*-


import arcade


class Game(arcade.Window):
    """Main game class."""

    def __init__(
        self,
        width,
        height,
        title,
        grid,
        map_objects,
    ):
        super().__init__(width, height, title)
        self.background_color = arcade.color.DARK_BLUE_GRAY
        self.grid = grid
        self.map_objects = map_objects

    def on_draw(self):
        self.clear()
        self.grid.sprite_list.draw()
        self.map_objects.sprite_list.draw()
