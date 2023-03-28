# -*- coding: utf-8 -*-


from . import constants


class AttackEffect:
    """
    Every AttackEffect instance have: a target_pattern attribute, that shows where attacker may target,
    affected_pattern attirbute, that shows what entities will be be affected on attack,
    and perform method, where goes all the code related to decreasing hp, pushing enemies around etc.

    Parameters (built by by builders):
    ----------------------------------
    target_positions
        List of coords that attacker may target (in other words, "where player can click to attack"). Represented
        by list of tuples. Attacker position is represented by (0, 0) and the coords are relative to its position.
        Attacker may choose only one tile to perform an attack.

    attack_pattern
        List of coords that will be attacked. Coords position are relative to the target_position. Multiple tiles
        may be affected.

    Methods:
    --------
    build_target_positions
        Assigns available target_positions to the AttackEffect.

    build_attack_pattern
        Assings list of coordinates that will be attacked in relation to selected target position.

    perform
        There goes all the code related to the actually performing an attack, so decreasing hp, pushing enemies, etc.
    """

    def __init__(self):
        self.build_target_positions()
        self.build_attack_pattern()

    def build_target_positions(self):
        raise NotImplementedError

    def build_attack_pattern(self):
        raise NotImplementedError


class PunchLeftAttackEffect(AttackEffect):
    def build_target_positions(self):
        self.target_positions = [
            (-1, 0),
        ]

    def build_attack_pattern(self):
        """
        T
        """
        self.attack_pattern = [
            (0, 0),
        ]

    def perform(self, beings, map_objects, x, y):
        for cell in self.attack_pattern:
            nx = x + cell[0]
            ny = y + cell[1]
            try:
                beings.find_being_by_cell_position(
                    nx,
                    ny,
                ).hp -= 1
            except AttributeError:
                pass  # Do not act if being is not found.
            try:
                predecessor = map_objects.find_map_object_by_cell_position(nx, ny)
                successor = predecessor.destroy()
                if successor:
                    map_objects.replace_map_object(predecessor, successor)
            except AttributeError:
                pass


class PunchRightAttackEffect(PunchLeftAttackEffect):
    def build_target_positions(self):
        self.target_positions = [
            (1, 0),
        ]


class PunchTopAttackEffect(PunchLeftAttackEffect):
    def build_target_positions(self):
        self.target_positions = [
            (0, 1),
        ]


class PunchBottomAttackEffect(PunchLeftAttackEffect):
    def build_target_positions(self):
        self.target_positions = [
            (0, -1),
        ]


class SidePunchLeftAttackEffect(PunchLeftAttackEffect):
    def build_attack_pattern(self):
        self.attack_pattern = [
            (0, -1),
            (0, 1),
        ]


class SidePunchRightAttackEffect(PunchRightAttackEffect):
    def build_attack_pattern(self):
        self.attack_pattern = [
            (0, -1),
            (0, 1),
        ]


class SidePunchTopAttackEffect(PunchTopAttackEffect):
    def build_attack_pattern(self):
        self.attack_pattern = [
            (-1, 0),
            (1, 0),
        ]


class SidePunchBottomAttackEffect(PunchBottomAttackEffect):
    def build_attack_pattern(self):
        self.attack_pattern = [
            (-1, 0),
            (1, 0),
        ]


class WallPunchLeftAttackEffect(SidePunchLeftAttackEffect):
    def build_attack_pattern(self):
        self.attack_pattern = [
            (0, -1),
            (0, 0),
            (0, 1),
        ]


class WallPunchRightAttackEffect(SidePunchRightAttackEffect):
    def build_attack_pattern(self):
        self.attack_pattern = [
            (0, -1),
            (0, 0),
            (0, 1),
        ]


class WallPunchTopAttackEffect(SidePunchTopAttackEffect):
    def build_attack_pattern(self):
        self.attack_pattern = [
            (-1, 0),
            (0, 0),
            (1, 0),
        ]


class WallPunchBottomAttackEffect(SidePunchBottomAttackEffect):
    def build_attack_pattern(self):
        self.attack_pattern = [
            (-1, 0),
            (0, 0),
            (1, 0),
        ]


def construct_attack_effects(cls):
    attack_effect = cls()
    attack_effect.build_target_positions()
    attack_effect.build_attack_pattern()
    return attack_effect
