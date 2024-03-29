# -*- coding: utf-8 -*-


import enum


class State(enum.Enum):
    GENERATE_MAP = enum.auto()
    PRESS_ANY_KEY = enum.auto()
    PLAY = enum.auto()
    MOVE = enum.auto()
    PLAYER_MOVE_ANIMATION = enum.auto()
    TARGET = enum.auto()
    ENEMY_TURN = enum.auto()
    ENEMY_ATTACK = enum.auto()
