# -*- coding: utf-8 -*-


# AI for enemy beings is being developed using TDD process.


from . import constants
from .components.position import Position
from .pathfinding import Pathfinder


class BaseAI:
    """
    BaseAI is a standard AI for enemy being.
    At first, AI is gathering informations about current map situation. Taking into account its owner position,
    player beings position and state, and position of targetable MapObject instances, it calculates the owner's
    priorities, then acts.

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
        # TODO: If nothing interesting is in range, then owner should move towards any goal.
        # Zero self.info.
        self.info = []
        next_to = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        # Set up pathfinder.
        pathfinder = Pathfinder(grid)
        pathfinder.set_up_path_grid(beings)
        # Iterate over all MapObject instances on game map.
        for map_object in grid.map_objects.objects:
            if not map_object.target:
                # Skill MapObject instances that are not marked as a targets.
                continue
            # Find all positions next to the MapObject,
            # because most MapObjects are marked as inaccessible so
            # pathfinder returns empty path then.
            neighbours = []
            for n in next_to:
                x = map_object.cell_position.x + n[0]
                y = map_object.cell_position.y + n[1]
                if 0 <= x <= 7 and 0 <= y <= 7:
                    # Add only Positions that are in map bounds.
                    neighbours.append(Position(x, y))
            paths_tmp = []
            # Find paths to neighbour tiles, then add only paths in range of owner.
            # (+1 because Pathfider takes into account tile under Being, too).
            for pos in neighbours:
                pathfinder.clean_up_path_grid()
                pathfinder.find_path(
                    self.owner.cell_position,
                    pos,
                )
                if pathfinder.last_path and len(pathfinder.last_path) <= self.owner.range + 1:
                    paths_tmp.append(pathfinder.last_path)
            # Find shortest path from all paths in range, then calculate priority, and add to self.info.
            if paths_tmp:
                path = (min(paths_tmp, key=len))
                priority = constants.AI_BUILDING_PRIORITY - (constants.AI_RANGE_FALLOFF * len(path))
                self.info.append([priority, map_object])
        # Iterate over all player Being instances on game map.
        for player in beings.player_beings:
            neighbours = []
            neighbours_tmp = []
            # Find all positions next to the player Being,
            # Being instances are marked as inaccessible so
            # pathfinder returns empty path then.
            for n in next_to:
                x = player.cell_position.x + n[0]
                y = player.cell_position.y + n[1]
                if 0 <= x <= 7 and 0 <= y <= 7:
                    neighbours.append(Position(x, y))
                    neighbours_tmp.append((x, y))
            paths_tmp = []
            # Find paths to neighbour tiles, then add only paths in range of owner.
            # (+1 because Pathfider takes into account tile under Being, too).
            for pos in neighbours:
                pathfinder.clean_up_path_grid()
                pathfinder.find_path(
                    self.owner.cell_position,
                    pos,
                )
                if pathfinder.last_path and len(pathfinder.last_path) <= self.owner.range + 1:
                    paths_tmp.append(pathfinder.last_path)
            # Find shortest path from all paths in range, then calculate priority, and add to self.info.
            if paths_tmp:
                path = (min(paths_tmp, key=len))
                if player.hp == 1:
                    priority = constants.AI_KILL_PLAYER_PRIORITY - (constants.AI_RANGE_FALLOFF * len(path))
                    self.info.append([priority, player])
                elif player.hp > 1:
                    priority = constants.AI_ATTACK_PLAYER_PRIORITY - (constants.AI_RANGE_FALLOFF * len(path))
                    self.info.append([priority, player])
