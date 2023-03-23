# -*- coding: utf-8 -*-


# AI for enemy beings is being developed using TDD process.


from . import constants
from .components.position import Position
from .map_object import MapObject
from .pathfinding import Pathfinder


class BaseAI:
    """
    BaseAI is a standard AI for enemy being.
    At first, AI is gathering informations about current map situation. Taking into account its owner position,
    tiles that owner can attack, player beings position and state, and position of targetable MapObject instances,
    it calculates the owner's priorities, then acts.

    Attributes:
    ----------
    owner: Being
        Enemy Being, owner of this AI instance.
    info: list of [int, Being | MapObject]
        In 'info' AI stores all MapObject and Being instances and calculated priorities.

    Methods:
    --------
    gather_map_info (Grid, Beings)
        This method populates info attribute. It iterates over Beings and MapObjects, finds the shortest valid path
        to every Being and MapObject, filters out targets that are outside the owner range, then calculates
        priority.
    """

    def __init__(self, owner):
        self.owner = owner
        self.info = []

    def gather_map_info(self, grid, beings):
        # Zero self.info.
        self.info = []
        attackable = self.owner.attack.return_attackable_positions(True)
        # Set up pathfinder.
        pathfinder = Pathfinder(grid)
        pathfinder.set_up_path_grid(beings)
        paths_backup = []
        # Iterate over all MapObject instances on game map.
        for map_object in grid.map_objects.objects:
            if not map_object.target:
                # Skip MapObject instances that are not marked as a targets.
                continue
            # Find all positions that owner can attack.
            neighbours = []
            for coords in attackable:
                x = map_object.cell_position.x + coords[0]
                y = map_object.cell_position.y + coords[1]
                if 0 <= x <= 7 and 0 <= y <= 7:
                    # Add only Positions that are in map bounds.
                    neighbours.append(Position(x, y))
            paths = []
            # Find paths to neighbour tiles, then add only paths in range of owner.
            # (+1 because Pathfider takes into account tile under Being, too).
            for pos in neighbours:
                pathfinder.clean_up_path_grid()
                pathfinder.find_path(
                    self.owner.cell_position,
                    pos,
                )
                if pathfinder.last_path:
                    if len(pathfinder.last_path) <= self.owner.range + 1:
                        paths.append(pathfinder.last_path)
                    else:
                        paths_backup.append(pathfinder.last_path)
            # Find shortest path from all paths in range, then calculate priority, and add to self.info.
            if paths:
                path = min(paths, key=len)
                priority = constants.AI_BUILDING_PRIORITY - (
                    constants.AI_RANGE_FALLOFF * len(path)
                )
                self.info.append([priority, map_object, path])
        # Iterate over all player Being instances on game map.
        for player in beings.player_beings:
            neighbours = []
            # Find all positions that owner Being can attack.
            for coords in attackable:
                x = player.cell_position.x + coords[0]
                y = player.cell_position.y + coords[1]
                if 0 <= x <= 7 and 0 <= y <= 7:
                    neighbours.append(Position(x, y))
            paths = []
            # Find paths to neighbour tiles, then add only paths in range of owner.
            # (+1 because Pathfider takes into account tile under Being, too).
            for pos in neighbours:
                pathfinder.clean_up_path_grid()
                pathfinder.find_path(
                    self.owner.cell_position,
                    pos,
                )
                if pathfinder.last_path:
                    if len(pathfinder.last_path) <= self.owner.range + 1:
                        paths.append(pathfinder.last_path)
                    else:
                        paths_backup.append(pathfinder.last_path)
            # Find shortest path from all paths in range, then calculate priority, and add to self.info.
            if paths:
                path = min(paths, key=len)
                if player.hp == 1:
                    priority = constants.AI_KILL_PLAYER_PRIORITY - (
                        constants.AI_RANGE_FALLOFF * len(path)
                    )
                    self.info.append([priority, player, path])
                elif player.hp > 1:
                    priority = constants.AI_ATTACK_PLAYER_PRIORITY - (
                        constants.AI_RANGE_FALLOFF * len(path)
                    )
                    self.info.append([priority, player, path])
        if not self.info and paths_backup:
            path = min(paths_backup, key=len)
            if path:
                # Path too long, slice to the owner.range.
                self.info.append(
                    [constants.AI_WALK_PRIORITY, 0, path[: self.owner.range + 1]]
                )

    def _sort_priorities(self):
        self.info.sort(key=lambda x: -x[0])

    def decide(self, grid):
        if not self.info:
            return "nothing"
        self._sort_priorities()
        target = self.info[0]
        target_type = type(target[constants.AI_INFO_ORDER_OBJECT])
        coords = target[constants.AI_INFO_ORDER_PATH][-1]
        self.owner.move_to(coords[0], coords[1])
        if target_type is int:
            return "walk"
        elif target_type is MapObject:
            new_tile = target[constants.AI_INFO_ORDER_OBJECT].destroy()
            grid.map_objects.replace_map_object(
                target[constants.AI_INFO_ORDER_OBJECT],
                new_tile,
            )
            return "attack_building"
        target[constants.AI_INFO_ORDER_OBJECT].hp -= 1
        print(target[constants.AI_INFO_ORDER_OBJECT].hp)
        return "attack_player"
