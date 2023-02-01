# -*- coding: utf-8 -*-


import arcade

import game.constants
import game.game
import game.grid


if __name__ == "__main__":
    grid = game.grid.Grid()
    game = game.game.Game(
        game.constants.SCREEN_WIDTH,
        game.constants.SCREEN_HEIGHT,
        game.constants.SCREEN_TITLE,
        grid,
    )
    print(len(game.grid.grid_sprite_list))
    arcade.run()
