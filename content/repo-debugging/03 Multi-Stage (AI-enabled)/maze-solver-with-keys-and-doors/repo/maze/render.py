"""Text output for solved mazes."""

from typing import Optional, Sequence

from .models import OPEN, Cell, Maze

PATH_MARK = "*"


def render_path(maze: Maze, path: Sequence[Cell] = ()) -> str:
    """Return the maze as text with the route drawn as ``*`` on floor cells.

    Start, goal, keys, doors and walls keep their own symbol.
    """
    marked = set(path)
    lines = []
    for r, row in enumerate(maze.grid):
        chars = []
        for c, ch in enumerate(row):
            chars.append(PATH_MARK if (r, c) in marked and ch == OPEN else ch)
        lines.append("".join(chars))
    return "\n".join(lines)


def format_solution(maze: Maze, path: Optional[Sequence[Cell]]) -> str:
    """Return the step count followed by the drawn route, or ``No path``."""
    if path is None:
        return "No path"
    return f"Steps: {len(path) - 1}\n{render_path(maze, path)}"
