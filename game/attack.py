# -*- coding: utf-8 -*-


from .components.position import Position


class Attack:
    """
    Attacks are performed by Being instances. Every Attack may consist of multiple AttackEffect instances.
    E.g. if we would like to add an Attack that damages the targeted Being, and pushes all adjacent Being instances
    from the target, then we could achieve that by making an Attack with two effects: first, that decreases HP of
    targeted Being, and second, that pushes away Being instances from the targeted Tile
    Before performing an attack, it checks if cursor position is valid as effect target position.
    """

    def __init__(self, *args):
        self.effects = args
        self.owner = None

    def perform(self, beings, x, y):
        if self.owner.attacked:
            return
        performed = False
        for effect in self.effects:
            cursor_position = Position(x, y).return_px_to_cell()
            valid_target_positions = []
            for target in effect.target_positions:
                valid_target_position = (
                    self.owner.cell_position.x + target[0],
                    self.owner.cell_position.y + target[1],
                )
                valid_target_positions.append(valid_target_position)
            if (cursor_position.x, cursor_position.y) in valid_target_positions:
                effect.perform(beings, x, y)
                performed = True
        self.owner.attacked = performed
