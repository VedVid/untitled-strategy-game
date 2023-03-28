# -*- coding: utf-8 -*-


from .components.position import Position


class Attack:
    """
    Attacks are performed by Being instances. Every Attack may consist of multiple AttackEffect instances.
    E.g. if we would like to add an Attack that damages the targeted Being, and pushes all adjacent Being instances
    from the target, then we could achieve that by making an Attack with two effects: first, that decreases HP of
    targeted Being, and second, that pushes away Being instances from the targeted Tile
    Before performing an attack, it checks if cursor position is valid as effect target position.
    If cursor argument is True (as is default, and remains True for player targeting), then x, y arguments
    are transformed from px to cells. Otherwise (e.g. after ai decides to attack) perform method assumes that cell-based
    coords has been passed.
    """

    def __init__(self, *args):
        self.effects = args
        self.owner = None

    def perform(self, beings, map_objects, x, y, cursor=True):
        if self.owner.attacked:
            return
        performed = False
        for effect in self.effects:
            cursor_position = Position(x, y).return_px_to_cell()
            if not cursor:
                cursor_position = Position(x, y)
            valid_target_positions = []
            for target in effect.target_positions:
                valid_target_position = (
                    self.owner.cell_position.x + target[0],
                    self.owner.cell_position.y + target[1],
                )
                valid_target_positions.append(valid_target_position)
            if (cursor_position.x, cursor_position.y) in valid_target_positions:
                effect.perform(beings, map_objects, x, y)
                performed = True
        if performed:
            self.owner.attacked = True
            self.owner.moved = True

    def return_attackable_positions(
        self, owner_position_agnostic=False, x=None, y=None
    ):
        # TODO: I think it could be used in SpriteTracker, too!
        positions = []
        for effect in self.effects:
            for target in effect.target_positions:
                for pattern in effect.attack_pattern:
                    pos_x = self.owner.cell_position.x
                    pos_y = self.owner.cell_position.y
                    if owner_position_agnostic:
                        pos_x = 0
                        pos_y = 0
                    if x and y:
                        pos_x = x
                        pos_y = y
                    target_position = (
                        pos_x + target[0] + pattern[0],
                        pos_y + target[1] + pattern[1],
                    )
                    positions.append(target_position)
        return positions
