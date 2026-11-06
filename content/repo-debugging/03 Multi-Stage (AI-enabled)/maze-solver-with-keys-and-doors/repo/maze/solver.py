"""Shortest-path search through a maze with keys and doors."""

from typing import List, Optional

from .models import Cell, Maze


def shortest_path(maze: Maze) -> Optional[List[Cell]]:
    """Return the shortest route from ``maze.start`` to ``maze.goal``.

    The route is a list of ``(row, col)`` cells that includes both the start
    and the goal. Stepping on a key (``a``-``f``) collects it; a door
    (``A``-``F``) can only be entered once the key with the same letter has
    been collected. Returns None if the goal cannot be reached.
    """
    raise NotImplementedError("shortest_path is not implemented yet")
