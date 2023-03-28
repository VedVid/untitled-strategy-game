# -*- coding: utf-8 -*-


import random

import arcade

from game import constants
from game.beings import Beings
from game.game import Game
from game.grid import Grid
from game.seeding import make_seed


game_seed = make_seed(4, 4)
random.seed(game_seed)
print(game_seed)

grid = Grid()

beings = Beings()

g = Game(
    constants.SCREEN_WIDTH,
    constants.SCREEN_HEIGHT,
    constants.SCREEN_TITLE,
    grid,
    beings,
)

g.beings.owner = g


if __name__ == "__main__":
    arcade.run()
