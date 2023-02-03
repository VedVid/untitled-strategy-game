# -*- coding: utf-8 -*-


import enum


class State(enum.Enum):
    GENERATE_MAP = enum.auto()
    PLAY = enum.auto()
