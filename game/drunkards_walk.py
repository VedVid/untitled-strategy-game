# -*- coding: utf-8 -*-


import random

from . import constants


class DrunkardsWalk:
    """
    Drunkard's walk is a procedural generation algorithm that digs through the filled map to create corridors.
    By default - and that it works here right now - it just choose the random direction to take the step, hence name.
    To improve the results, one could add some heuristic, or additional checks after the level is created to make sure
    that the result is viable map, or use stack of empty tiles as described here:
    https://www.reddit.com/r/roguelikedev/comments/hhzszb/comment/fwd5h2j/?utm_source=share&utm_medium=web2x&context=3.

    Parameters:
    -----------
    owner: grid
        Instance of Grid class that calls DrunkardsWalk.
    start_x, start_y: int
        Starting coords of walker. If not provided, coords will be created randomly within
        grid width and height.
    steps: int
        Number of steps that walker will take. If None is passed, steps take random value generated within
        bounds specified in constants file.

    Methods:
    --------
    walk
        Starts the algorithm
    """

    def __init__(self, owner, start_x=None, start_y=None, steps=None):
        self.owner = owner
        self.start_x = start_x
        if self.start_x is None:
            self.start_x = random.randint(0, self.owner.width - 1)
        self.start_y = start_y
        if self.start_y is None:
            self.start_y = random.randint(0, self.owner.height - 1)
        self.steps = steps
        if self.steps is None:
            self.steps = random.randint(
                constants.DIG_PERCENT_MIN, constants.DIG_PERCENT_MAX
            )
        # Adjust the value below if you wish to allow diagonal movement.
        self.directions = [
            [0, 1],
            [-1, 0],
            [1, 0],
            [0, -1],
        ]

    def walk(self):
        """
        Starts the algorithm at the given coordinates, then moves step-by-step, horizontally or vertically.
        If new coords are valid (within the owner (grid) bounds), then remove the MapObject from this map cell.
        The walker will walk until all steps are taken.
        """
        # cur_x and cur_y are coords of Tile currently occupied by walker.
        cur_x = self.start_x
        cur_y = self.start_y
        while self.steps > 0:
            # Check if there is an instance of MapObject here...
            obj = next(
                (
                    obj
                    for obj in self.owner.map_objects.objects
                    if (obj.cell_position.x == cur_x and obj.cell_position.y == cur_y)
                ),
                None,
            )
            # ...and if it is, then remove the object from the list and decrement steps.
            if obj:
                self.owner.map_objects.remove_map_object(obj)
                self.steps -= 1
            # Continue even if the Tile has been cleared already.
            # Choose a new direction, and update cur_x and cur_y if valid.
            direction = random.choice(self.directions)
            new_x = cur_x + direction[0]
            new_y = cur_y + direction[1]
            if 0 <= new_x < self.owner.width and 0 <= new_y < self.owner.height:
                cur_x = new_x
                cur_y = new_y
