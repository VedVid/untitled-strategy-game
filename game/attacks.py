# -*- coding: utf-8 -*-


from .attack import Attack
from . import attack_effect as ae


attack_punch = Attack(
    ae.construct_attack_effects(ae.PunchLeftAttackEffect),
    ae.construct_attack_effects(ae.PunchRightAttackEffect),
    ae.construct_attack_effects(ae.PunchTopAttackEffect),
    ae.construct_attack_effects(ae.PunchBottomAttackEffect),
)

attack_side_punch = Attack(
    ae.construct_attack_effects(ae.SidePunchLeftAttackEffect),
    ae.construct_attack_effects(ae.SidePunchRightAttackEffect),
    ae.construct_attack_effects(ae.SidePunchTopAttackEffect),
    ae.construct_attack_effects(ae.SidePunchBottomAttackEffect),
)

attack_wall_punch = Attack(
    ae.construct_attack_effects(ae.WallPunchLeftAttackEffect),
    ae.construct_attack_effects(ae.WallPunchRightAttackEffect),
    ae.construct_attack_effects(ae.WallPunchTopAttackEffect),
    ae.construct_attack_effects(ae.WallPunchBottomAttackEffect),
)
