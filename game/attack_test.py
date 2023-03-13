# -*- coding: utf-8 -*-


from .attack import Attack
from . import attack_effect as ae
from .being import Player, construct_beings


attack_1 = Attack(
    ae.construct_attack_effects(ae.PunchAttackEffect),
)

attack_2 = Attack(
    ae.construct_attack_effects(ae.WallPunchVerAttackEffect),
    ae.construct_attack_effects(ae.SidePunchHorAttackEffect),
)

player_1 = construct_beings(Player, 5, 5)
player_1.attack = attack_1
player_2 = construct_beings(Player, 3, 3)
player_2.attack = attack_2


def test_amount_of_attack_effects_separate():
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


def test_amount_of_attack_effects_bound_to_being():
    assert len(player_1.attack.effects) == 1
    assert len(player_2.attack.effects) == 2


def test_type_of_effects_bound_to_being():
    assert type(player_1.attack.effects[0]) is ae.PunchAttackEffect
    assert type(player_2.attack.effects[0]) is ae.WallPunchVerAttackEffect
    assert type(player_2.attack.effects[1]) is ae.SidePunchHorAttackEffect


def test_tiles_targeted_bound_to_being():
    targeted_tiles_1 = []
    for coords in player_1.attack.effects[0].target_positions:
        targeted_tiles_1.append(
            (
                player_1.cell_position.x + coords[0],
                player_1.cell_position.y + coords[1],
            )
        )
    assert all(x in [(4, 5), (6, 5), (5, 4), (5, 6)] for x in targeted_tiles_1)
    targeted_tiles_2 = []
    for coords in player_2.attack.effects[0].target_positions:
        targeted_tiles_2.append(
            (
                player_2.cell_position.x + coords[0],
                player_2.cell_position.y + coords[1],
            )
        )
    assert all(x in [(3, 2), (3, 4)] for x in targeted_tiles_2)
    targeted_tiles_3 = []
    for coords in player_2.attack.effects[1].target_positions:
        targeted_tiles_3.append(
            (
                player_2.cell_position.x + coords[0],
                player_2.cell_position.y + coords[1],
            )
        )
    assert all(x in [(2, 3), (4, 3)] for x in targeted_tiles_3)
    assert not any(x in targeted_tiles_2 for x in targeted_tiles_3)


def test_attack_patterns_bound_to_being():
    pattern_1 = []
    for coords1 in player_1.attack.effects[0].target_positions:
        for coords2 in player_1.attack.effects[0].attack_pattern:
            pattern_1.append(
                (
                    player_1.cell_position.x + coords1[0] + coords2[0],
                    player_1.cell_position.y + coords1[1] + coords2[1],
                )
            )
    assert all(x in [(4, 5), (6, 5), (5, 4), (5, 6)] for x in pattern_1)
    pattern_2 = []
    for coords1 in player_2.attack.effects[0].target_positions:
        for coords2 in player_2.attack.effects[0].attack_pattern:
            pattern_2.append(
                (
                    player_2.cell_position.x + coords1[0] + coords2[0],
                    player_2.cell_position.y + coords1[1] + coords2[1],
                )
            )
    assert all(x in [(2, 2), (3, 2), (4, 2), (2, 4), (3, 4), (4, 4)] for x in pattern_2)
    pattern_3 = []
    for coords1 in player_2.attack.effects[1].target_positions:
        for coords2 in player_2.attack.effects[1].attack_pattern:
            pattern_3.append(
                (
                    player_2.cell_position.x + coords1[0] + coords2[0],
                    player_2.cell_position.y + coords1[1] + coords2[1],
                )
            )
    assert all(x in [(2, 4), (2, 2), (4, 4), (4, 2)] for x in pattern_3)
