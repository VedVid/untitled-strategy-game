# -*- coding: utf-8 -*-


# AI for enemy beings is being developed using TDD process.


import copy

from . import constants
from .attacks import attack_side_punch, attack_wall_punch
from .being import construct_beings, Enemy, Player
from .beings import Beings
from .grid import Grid
from .map_object import MapObject
from .map_objects import MapObjects


class TestAI:
    """
    K......P
    ...3....
    1......2
    ........
    ...5....
    ........
    B.......
    6B.T.4..
    where T -> building, P -> player at full health, K -> nearly killed player,
    1-6 -> enemies;
    1: has only K in range
    2: has only P in range
    3: has all K, P and T in range
    4: has only T in range
    5: has a very short movement range and no tile / entity is in its range
    6: is blocked by MapObject instances that are not targetable
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
    blocking1 = MapObject(
        0,
        1,
        "test.png",
        "test_selected.png",
        "test_targeted.png",
        blocks=True,
        target=False,
    )
    blocking2 = MapObject(
        1,
        0,
        "test.png",
        "test_selected.png",
        "test_targeted.png",
        blocks=True,
        target=False,
    )
    map_objects.add_map_object(building)
    map_objects.add_map_object(blocking1)
    map_objects.add_map_object(blocking2)
    grid = Grid(width=8, height=8, map_objects=map_objects)
    k = construct_beings(Player, 0, 7)
    k.hp = 1
    p = construct_beings(Player, 7, 7)
    e1 = construct_beings(Enemy, 0, 5)
    e1.attack = copy.copy(attack_side_punch)
    e1.attack.owner = e1
    e2 = construct_beings(Enemy, 7, 5)
    e3 = construct_beings(Enemy, 3, 6)
    e3.attack = copy.copy(attack_wall_punch)
    e3.attack.owner = e3
    e4 = construct_beings(Enemy, 5, 0)
    e5 = construct_beings(Enemy, 3, 3)
    e5.range = 1
    e6 = construct_beings(Enemy, 0, 0)
    beings = Beings()
    beings.player_beings.append(k)
    beings.player_beings.append(p)

    def test_ai_1(self):
        self.e1.ai.gather_map_info(self.grid, self.beings)
        assert self.e1.ai.decide(self.grid) == "attack_player"
        assert self.e1.cell_position.x == 1 and self.e1.cell_position.y == 6
        assert len(self.e1.ai.info) == 1
        assert self.e1.ai.info[0][constants.AI_INFO_ORDER_PRIORITY] == 4
        assert type(self.e1.ai.info[0][constants.AI_INFO_ORDER_OBJECT]) is Player
        assert len(self.e1.ai.info[0][constants.AI_INFO_ORDER_PATH]) == 3

    def test_ai_2(self):
        self.e2.ai.gather_map_info(self.grid, self.beings)
        assert self.e2.ai.decide(self.grid) == "attack_player"
        assert self.e2.cell_position.x == 7 and self.e2.cell_position.y == 6
        assert len(self.e2.ai.info) == 1
        assert self.e2.ai.info[0][constants.AI_INFO_ORDER_PRIORITY] == 3
        assert type(self.e2.ai.info[0][constants.AI_INFO_ORDER_OBJECT]) is Player
        assert len(self.e2.ai.info[0][constants.AI_INFO_ORDER_PATH]) == 2

    def test_ai_3(self):
        self.e3.ai.gather_map_info(self.grid, self.beings)
        assert self.e3.ai.decide(self.grid) == "attack_player"
        assert self.e3.cell_position.x == 1 and self.e3.cell_position.y == 6
        assert len(self.e3.ai.info) == 3
        assert self.e3.ai.info[0][constants.AI_INFO_ORDER_PRIORITY] == 4
        assert self.e3.ai.info[1][constants.AI_INFO_ORDER_PRIORITY] == 2
        assert self.e3.ai.info[2][constants.AI_INFO_ORDER_PRIORITY] == 1
        assert type(self.e3.ai.info[0][constants.AI_INFO_ORDER_OBJECT]) is Player
        assert type(self.e3.ai.info[1][constants.AI_INFO_ORDER_OBJECT]) is MapObject
        assert type(self.e3.ai.info[2][constants.AI_INFO_ORDER_OBJECT]) is Player
        assert len(self.e3.ai.info[0][constants.AI_INFO_ORDER_PATH]) == 3
        assert len(self.e3.ai.info[1][constants.AI_INFO_ORDER_PATH]) == 6
        assert len(self.e3.ai.info[2][constants.AI_INFO_ORDER_PATH]) == 4

    def test_ai_4(self):
        self.e4.ai.gather_map_info(self.grid, self.beings)
        assert self.e4.ai.decide(self.grid) == "attack_building"
        assert self.e4.cell_position.x == 4 and self.e4.cell_position.y == 0
        assert len(self.e4.ai.info) == 1
        assert self.e4.ai.info[0][constants.AI_INFO_ORDER_PRIORITY] == 6
        assert type(self.e4.ai.info[0][constants.AI_INFO_ORDER_OBJECT]) is MapObject
        assert len(self.e4.ai.info[0][constants.AI_INFO_ORDER_PATH]) == 2

    def test_ai_5(self):
        self.e5.ai.gather_map_info(self.grid, self.beings)
        assert self.e5.ai.decide(self.grid) == "walk"
        assert self.e5.cell_position.x == 3 and self.e5.cell_position.y == 2
        assert len(self.e5.ai.info) == 1
        assert self.e5.ai.info[0][constants.AI_INFO_ORDER_PRIORITY] == 1
        assert type(self.e5.ai.info[0][constants.AI_INFO_ORDER_OBJECT]) is int
        assert len(self.e5.ai.info[0][constants.AI_INFO_ORDER_PATH]) == 2

    def test_ai_6(self):
        self.e6.ai.gather_map_info(self.grid, self.beings)
        assert self.e6.ai.decide(self.grid) == "nothing"
        assert self.e6.cell_position.x == 0 and self.e6.cell_position.y == 0
        assert len(self.e6.ai.info) == 0
