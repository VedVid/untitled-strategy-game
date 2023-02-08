# -*- coding: utf-8 -*-


# Using the Singleton / Borg pattern.
# Source: https://github.com/faif/python-patterns/blob/master/patterns/creational/borg.py
# and https://code.activestate.com/recipes/66531/
# Maybe pathfinding is not the best use case for the Borg pattern, as it will create a lot of instances
# and it may take a lot of memory.
# But for the sake of learning, it fits nicely.


from pathfinding.core.grid import Grid as PathGrid
from pathfinding.finder.breadth_first import BreadthFirstFinder

from . import constants


# TODO: Remember to set up finder clean-up somewhere! Please read below the fragment of library documentation.
# While running the pathfinding algorithm it might set values on the nodes. Depending on your path finding algorithm
# things like calculated distances or visited flags might be stored on them. So if you want to run the algorithm
# in a loop you need to clean the grid first (see Grid.cleanup). Please note that because cleanup looks at all nodes
# of the grid it might be an operation that can take a bit of time!
class Pathfinder:
    """
    Class Pathfinder is a Borg used for finding paths the shortest paths between two points on the map.
    Will be used by AI, also for rendering the path from PC to cursor on the mouse move, and to check if the newly
    generated map is not too convulated.
    Uses Breadth-First Search algorithm - totally sufficient if diagonal movement is forbidden. Otherwise, A* may
    be a better choice.

    Parameters:
    ===========
    grid: Grid
        Already existing instance of Grid. Used to create matrix required by pathfinding package.

    Methods:
    ========
    _make_matrix (Grid): 2d list
        Uses Grid to create matrix required by pathfinding package.
    _set_up_path_grid: None or PathGrid
        Creates new PathGrid instance or cleans up existing PathGrid instance.
    clean_up_path_grid
        Cleans up the Grid. Necessary to rerunning the pathfinding algorithm.
    find_path (Position, Position): list of sets, int
        Finds path between first Position and second Position.
    """

    _shared_state = {}

    def __init__(self, grid):
        self.__dict__ = self._shared_state
        self.grid = grid
        self._matrix = self._make_matrix(grid)
        self._path_grid = self._set_up_path_grid()
        self.finder = BreadthFirstFinder()

    @staticmethod
    def _make_matrix(grid):
        """Uses Grid to create matrix required by pathfinding package. '0' means empty tile, '1' indicates obstacle."""
        matrix = [[
            1
            for x in range(grid.width)]
            for y in range(grid.height)]
        for obj in grid.map_objects.objects:
            if obj.blocks:
                matrix[obj.cell_position.y][obj.cell_position.x] = 0
        # Arcade grid starts at the bottom-left corner. Reversing matrix ensures compatibility.
        matrix.reverse()
        return matrix

    def _set_up_path_grid(self):
        """Creates new PathGrid if not exists, performs cleanup otherwise."""
        try:
            if self._path_grid:
                self.clean_up_path_grid()
        except AttributeError:
            return PathGrid(matrix=self._matrix)

    def clean_up_path_grid(self):
        """Cleans up the Grid. Necessary when rerunning the algorithm."""
        self._path_grid.cleanup()

    def find_path(self, start_position, target_position):
        """
        Finds shortest path between two positions. Returns path (list of sets, every set is a coordinate of the step
        taken) and number of passes.
        Hacky position.y is result of how coords of arcade and pathfinding library work: arcade starts
        from the bottom-left corner, and pathfinding starts from the top-left corner.
        """
        start = self._path_grid.node(start_position.x, self.grid.width - 1 - start_position.y)
        target = self._path_grid.node(target_position.x, self.grid.height - 1 - target_position.y)
        path, runs = self.finder.find_path(start=start, end=target, grid=self._path_grid)
        return path, runs
