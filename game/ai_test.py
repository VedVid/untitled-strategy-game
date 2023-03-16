# -*- coding: utf-8 -*-


# AI for enemy beings is being developed using TDD process.


from . import being
from . import constants
from .ai import BaseAI
from .being import Player
from .beings import Beings
from .grid import Grid
from .map_object import MapObject
from .map_objects import MapObjects


class TestAI:
    """
    K..3...P
    ........
    1......2
    ........
    ..5.6...
    ........
    ........
    ...T.4..
    where T -> building, P -> player at full health, K -> nearly killed player,
    1-6 -> enemies;
    1: has only K in range
    2: has only P in range
    3: has both K and P in range
    4: has only T in range
    5: has very long movement range and every tile / entity is in its range
    6: has a very short movement range and no tile / entity is in its range
    """

    map_objects = MapObjects()
    ruins = MapObject(
        3,
        0,
        "test.png",
        "test_selected.png",
        "test_targeted.png",
        blocks=True,
        target=False,
        successor=None,
    )
    building = MapObject(
        3,
        0,
        "test.png",
        "test_selected.png",
        "test_targeted.png",
        blocks=True,
        target=True,
        successor=ruins,
    )
    map_objects.add_map_object(building)
    grid = Grid(width=8, height=8, map_objects=map_objects)
    k = being.construct_beings(being.Player, 0, 7)
    k.hp = 1
    p = being.construct_beings(being.Player, 7, 7)
    e1 = being.construct_beings(being.Enemy, 0, 5)
    e2 = being.construct_beings(being.Enemy, 7, 5)
    e3 = being.construct_beings(being.Enemy, 3, 7)
    e4 = being.construct_beings(being.Enemy, 5, 0)
    e5 = being.construct_beings(being.Enemy, 2, 3)
    e5.range = 10
    e6 = being.construct_beings(being.Enemy, 4, 3)
    e6.range = 1
    beings = Beings()
    beings.player_beings.append(k)
    beings.player_beings.append(p)

    def test_gather_info(self):
        self.e1.ai.gather_map_info(self.grid, self.beings)
        self.e2.ai.gather_map_info(self.grid, self.beings)
        self.e3.ai.gather_map_info(self.grid, self.beings)
        self.e4.ai.gather_map_info(self.grid, self.beings)
        self.e5.ai.gather_map_info(self.grid, self.beings)
        self.e6.ai.gather_map_info(self.grid, self.beings)
        priority = 0
        obj = 1
        assert len(self.e1.ai.info) == 1
        assert self.e1.ai.info[0][priority] == 4
        assert type(self.e1.ai.info[0][obj]) is Player
        assert len(self.e2.ai.info) == 1
        assert self.e2.ai.info[0][priority] == 2
        assert type(self.e2.ai.info[0][obj]) is Player
        assert len(self.e3.ai.info) == 2
        self.e3.ai.info.sort()
        assert self.e3.ai.info[0][priority] == 0
        assert type(self.e3.ai.info[0][obj]) is Player
        assert self.e3.ai.info[1][priority] == 3
        assert len(self.e4.ai.info) == 1
        assert self.e4.ai.info[0][priority] == 6
        assert len(self.e5.ai.info) == 3
        assert len(self.e6.ai.info) == 0
