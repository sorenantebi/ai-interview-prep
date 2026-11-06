"""Shortest-path search through a maze with keys and doors."""

from collections import deque
from typing import Dict, List, Optional, Tuple

from .keys import door_bit, is_door, is_key, key_bit
from .models import Cell, Maze

State = Tuple[Cell, int]


def _rebuild(parent: Dict[State, Optional[State]], state: State) -> List[Cell]:
    """Walk the parent links back from ``state`` and return the cell route."""
    cells = []
    current: Optional[State] = state
    while current is not None:
        cells.append(current[0])
        current = parent[current]
    cells.reverse()
    return cells


def shortest_path(maze: Maze) -> Optional[List[Cell]]:
    """Return the shortest route from ``maze.start`` to ``maze.goal``.

    The route is a list of ``(row, col)`` cells that includes both the start
    and the goal. Stepping on a key (``a``-``f``) collects it; a door
    (``A``-``F``) can only be entered once the key with the same letter has
    been collected. Returns None if the goal cannot be reached.
    """
    start: State = (maze.start, 0)
    parent: Dict[State, Optional[State]] = {start: None}
    queue = deque([start])
    grid = maze.grid
    while queue:
        state = queue.popleft()
        pos, mask = state
        if pos == maze.goal:
            return _rebuild(parent, state)
        for nxt in maze.neighbors(pos):
            ch = grid[nxt[0]][nxt[1]]
            if is_door(ch) and not mask & door_bit(ch):
                continue
            new_mask = mask | key_bit(ch) if is_key(ch) else mask
            new_state = (nxt, new_mask)
            if new_state not in parent:
                parent[new_state] = state
                queue.append(new_state)
    return None
