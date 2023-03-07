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


class PunchAttackEffect(AttackEffect):
    #TODO: Change "A" (Attacker) to "B" (Being).
    def build_target_positions(self):
        """
         T
        TAT
         T
        """
        self.target_positions = [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1),
        ]

    def build_attack_pattern(self):
        """
        T
        """
        self.attack_pattern = [
            (0, 0),
        ]

    def perform(self, beings, x, y):
        for cell in self.attack_pattern:
            try:
                beings.find_being_by_px_position(
                    x + (cell[0] * constants.TILE_SIZE_W),
                    y + (cell[1] * constants.TILE_SIZE_H),
                ).hp -= 1
            except AttributeError:
                pass  # Do not act if being is not found.


class SidePunchHorAttackEffect(PunchAttackEffect):
    def build_target_positions(self):
        """
        TBT
        """
        self.target_positions = [
            (-1, 0),
            (1, 0),
        ]

    def build_attack_pattern(self):
        """
        A
        T
        A
        """
        self.attack_pattern = [
            (0, -1),
            (0, 1),
        ]


class SidePunchVerAttackEffect(PunchAttackEffect):
    def build_target_positions(self):
        """
        TBT
        """
        self.target_positions = [
            (0, -1),
            (0, 1),
        ]

    def build_attack_pattern(self):
        """
        ATA
        """
        self.attack_pattern = [
            (-1, 0),
            (1, 0),
        ]


def construct_attack_effects(cls):
    attack_effect = cls()
    attack_effect.build_target_positions()
    attack_effect.build_attack_pattern()
    return attack_effect
