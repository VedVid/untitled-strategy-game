# -*- coding: utf-8 -*-


import random

from . import constants


class DrunkardsWalk:
    """Drunkard's walk is a procedural generation algorithm that digs through the filled map to create corridors.
    By default - and that it works here right now - it just choose the random direction to take the step, hence name.
    To improve the results, one could add some heuristic, or additional checks after the level is created to make sure
    that the result is viable map."""

    def __init__(
        self, owner, start_x=None, start_y=None, steps=constants.DRUNKARDS_WALK_STEPS
    ):
        self.owner = owner
        self.start_x = start_x
        if self.start_x is None:
            self.start_x = random.randint(0, self.owner.width - 1)
        self.start_y = start_y
        if self.start_y is None:
            self.start_y = random.randint(0, self.owner.height - 1)
        self.steps = steps
        # Adjust the value below if you wish to allow diagonal movement.
        self.directions = [-1, 1]

    def walk(self):
        cur_x = self.start_x
        cur_y = self.start_y
        for step in range(self.steps):
            new_x = cur_x + random.choice(self.directions)
            new_y = cur_y + random.choice(self.directions)
            if (
                new_x < 0
                or new_x >= self.owner.width
                or new_y < 0
                or new_y >= self.owner.height
            ):
                continue
            if random.choice(self.directions) == -1:  # horizontal
                cur_x = new_x
            else:  # vertical
                cur_y = new_y
            xx = (cur_x * constants.TILE_SIZE_W) + constants.TILE_CENTER_OFFSET_X
            yy = (cur_y * constants.TILE_SIZE_H) + constants.TILE_CENTER_OFFSET_Y
            obj = next(
                (
                    obj
                    for obj in self.owner.map_objects.objects
                    if (obj.position.x == xx and obj.position.y == yy)
                ),
                None,
            )
            if obj:
                self.owner.map_objects.remove_map_object(obj)
