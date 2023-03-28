# -*- coding: utf-8 -*-


# First version of AI has been developed using TDD.


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
        self.map_in_range = []
        self.map_out_range = []

    def gather_map_info(self, grid, beings):
        # Zero self.info.
        self.map_in_range = []
        self.map_out_range = []
        pathfinder = Pathfinder(grid)
        pathfinder.set_up_path_grid(beings)
        for tile in grid.tiles:
            data = {
                "tile": (tile.cell_position.x, tile.cell_position.y),
                "targets": None,
                "targetables": None,
                "affected": None,
                "priorities": None,
                "in range": True,
            }
            pathfinder.clean_up_path_grid()
            # Check availability of every tile.
            path, _ = pathfinder.find_path(
                    self.owner.cell_position,
                    tile.cell_position
            )
            if len(path) == 0:
                continue  # tile occupied by object, or no valid path to tile
            if len(path) > self.owner.range:
                data["in range"] = False
                data["tile"] = path[self.owner.range]
            b = beings.find_being_by_cell_position(tile.cell_position.x, tile.cell_position.y)
            if b and b is not self.owner:
                continue  # tile occupied by other being
            targetables = []
            all_affected_positions = []
            # Iterating over all attack effects of owner's attack,
            # in order to find all tiles that owner can target (so, "click on it") (stored in targetables)
            # and tiles that will be affected by attack.
            # Index of one element of all_affected_positions match index of element of targetables.
            for effect in self.owner.attack.effects:
                targetable_position = (
                    tile.cell_position.x + effect.target_positions[0][0],
                    tile.cell_position.y + effect.target_positions[0][1],
                )
                # Add only targetable positions that are within map bounds.
                if targetable_position[0] >= 0 and targetable_position[0] < constants.GRID_SIZE_W and \
                    targetable_position[1] >= 0 and targetable_position[1] < constants.GRID_SIZE_H:
                    targetables.append(targetable_position)
                    affected_positions = []
                    for element in effect.attack_pattern:
                        affected_position = (
                            targetable_position[0] + element[0],
                            targetable_position[1] + element[1],
                        )
                        # Add only these tiles that will be affected by attack and are within map bounds.
                        if affected_position[0] >= 0 and affected_position[0] < constants.GRID_SIZE_W and \
                            affected_position[1] >= 0 and affected_position[1] < constants.GRID_SIZE_H:
                            affected_positions.append(affected_position)
                    all_affected_positions.append(affected_positions)
            data["targetables"] = targetables
            data["affected"] = all_affected_positions
            # Calculate priority penalty for tile.
            range_priority_penalty = len(path) * constants.AI_RANGE_FALLOFF
            # Calculating priorities for every targetable tile.
            priorities = []
            targets = []
            for affected_tiles in all_affected_positions:
                priority = -range_priority_penalty
                for affected_tile in affected_tiles:
                    being = beings.find_being_by_cell_position(
                        affected_tile[0],
                        affected_tile[1],
                    )
                    map_object = grid.map_objects.find_map_object_by_cell_position(
                        affected_tile[0],
                        affected_tile[1],
                    )
                    if being:
                        if being in beings.enemy_beings:
                            priority -= constants.AI_ATTACK_OWN_PRIORITY
                        else:
                            targets.append(being)
                            if being.hp <= 0:
                                pass
                            elif being.hp == 1:  # TODO: Change to comparison with attack power!
                                priority += constants.AI_KILL_PLAYER_PRIORITY
                            else:
                                priority += constants.AI_ATTACK_PLAYER_PRIORITY
                    if map_object:
                        if map_object.target:
                            targets.append(map_object)
                            priority += constants.AI_BUILDING_PRIORITY
                priorities.append(priority)
            data["priorities"] = priorities
            data["targets"] = targets
            if data["in range"] and data["targets"]:
                self.map_in_range.append(data)
            else:
                self.map_out_range.append(data)

    def _sort_priorities_in_range(self):
        return sorted(self.map_in_range, key=lambda d: (max(d['priorities'])), reverse=True)

    def _sort_priorities_out_range(self):
        return sorted(self.map_out_range, key=lambda d: (max(d['priorities'])), reverse=True)

    def decide(self):
        in_range_sorted = self._sort_priorities_in_range()
        # There are targets in range.
        if len(in_range_sorted) > 0:
            self.owner.move_to(in_range_sorted[0]["tile"][0], in_range_sorted[0]["tile"][1])
            return in_range_sorted[0]
        out_range_sorted = self._sort_priorities_out_range()
        # There are no targets in range, but owner is not blocked and can move towards the targets.
        if len(out_range_sorted) > 0:
            self.owner.move_to(out_range_sorted[0]["tile"][0], out_range_sorted[0]["tile"][1])
            return out_range_sorted[0]
        return "nothing"
