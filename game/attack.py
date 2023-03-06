# -*- coding: utf-8 -*-


class Attack:
    """
    Attacks are performed by Being instances. Every Attack may consist of multiple AttackEffect instances.
    E.g. if we would like to add an Attack that damages the targeted Being, and pushes all adjacent Being instances
    from the target, then we could achieve that by making an Attack with two effects: first, that decreases HP of
    targeted Being, and second, that pushes away Being instances from the targeted Tile.
    """

    def __init__(self, *args):
        self.effects = args

    def perform(self, beings, x, y):
        for effect in self.effects:
            effect.perform(beings, x, y)
