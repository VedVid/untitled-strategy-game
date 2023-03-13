# -*- coding: utf-8 -*-


from .attack import Attack
from . import attack_effect as ae


attack_1 = Attack(
    ae.construct_attack_effects(ae.PunchAttackEffect),
)

attack_2 = Attack(
    ae.construct_attack_effects(ae.WallPunchVerAttackEffect),
    ae.construct_attack_effects(ae.SidePunchHorAttackEffect),
)


def test_amount_of_attack_effects():
    assert len(attack_1.effects) == 1
    assert len(attack_2.effects) == 2


def test_tiles_targeted_separate():
    assert all(x in [(-1, 0), (1, 0), (0, -1), (0, 1)] for x in attack_1.effects[0].target_positions)
    assert all(x in [(-1, 0), (1, 0), (0, -1), (0, 1)] for x in attack_2.effects[0].target_positions)
    assert all(x in [(-1, 0), (1, 0), (0, -1), (0, 1)] for x in attack_2.effects[1].target_positions)


def test_attack_pattern_separate():
    assert all(x in [(0, 0)] for x in attack_1.effects[0].attack_pattern)
    assert all(x in [(0, 0), (-1, 0), (1, 0)] for x in attack_2.effects[0].attack_pattern)
    assert all(x in [(0, -1), (0, 1)] for x in attack_2.effects[1].attack_pattern)
