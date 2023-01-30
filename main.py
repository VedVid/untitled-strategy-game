# -*- coding: utf-8 -*-


import game.grid


if __name__ == '__main__':
    grid = game.grid.Grid(8, 8)
    for tile in grid.tiles:
        print(f"[x: {tile.position.x}, y: {tile.position.y}, w: {tile.size.width}, h: {tile.size.height}]")
