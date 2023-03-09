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
        self.owner = None

    def perform(self, beings, x, y):
        print("\n---")
        for effect in self.effects:
            print()
            from .components.position import Position
            cursor_position = Position(x, y).return_px_to_cell()
            cursor_tuple = (cursor_position.x, cursor_position.y)
            owner_position = self.owner.cell_position
            valid_target_positions = []
            print("cursor_position:", cursor_position.x, cursor_position.y)
            print("owner_position :", owner_position.x, owner_position.y)
            print("valid target positions:")
            for target in effect.target_positions:
                valid_target_position = (
                    owner_position.x + target[0],
                    owner_position.y + target[1],
                )
                valid_target_positions.append(valid_target_position)
                print("   ", valid_target_position)
            if cursor_tuple in valid_target_positions:
                print(1)
                effect.perform(beings, x, y)
            else:
                print(0)
