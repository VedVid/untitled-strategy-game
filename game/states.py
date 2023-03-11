# -*- coding: utf-8 -*-


import enum


class State(enum.Enum):
    GENERATE_MAP = enum.auto()
    PLAY = enum.auto()
    MOVE = enum.auto()
    TARGET = enum.auto()
    ENEMY_TURN = enum.auto()
