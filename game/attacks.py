# -*- coding: utf-8 -*-


from .attack import Attack
from . import attack_effect as ae


attack_punch = Attack(
    ae.construct_attack_effects(ae.PunchAttackEffect),
)

attack_side_punch = Attack(
    ae.construct_attack_effects(ae.SidePunchHorAttackEffect),
    ae.construct_attack_effects(ae.SidePunchVerAttackEffect),
)
