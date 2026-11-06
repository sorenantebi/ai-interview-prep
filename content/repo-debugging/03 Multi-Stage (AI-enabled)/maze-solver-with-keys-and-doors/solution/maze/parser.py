"""Parsing of ASCII maze files."""

from typing import List, Tuple

from .keys import DOOR_LETTERS, KEY_LETTERS
from .models import GOAL, OPEN, START, WALL, Maze

ALLOWED = set(WALL + OPEN + START + GOAL + KEY_LETTERS + DOOR_LETTERS)


def _locate(lines: List[str], symbol: str) -> List[Tuple[int, int]]:
    """Return every position of ``symbol`` in the grid."""
    found = []
    for row, line in enumerate(lines):
        for col, ch in enumerate(line):
            if ch == symbol:
                found.append((row, col))
    return found


def parse_grid(text: str) -> Maze:
    """Parse ``text`` into a :class:`Maze`.

    Blank lines before and after the maze are ignored. Raises ValueError
    for ragged rows, unknown symbols, or a missing or duplicated start/goal.
    """
    lines = [line.rstrip() for line in text.splitlines()]
    while lines and not lines[0]:
        lines.pop(0)
    while lines and not lines[-1]:
        lines.pop()
    if not lines:
        raise ValueError("empty maze")

    width = len(lines[0])
    for index, line in enumerate(lines):
        if len(line) != width:
            raise ValueError(f"row {index} has length {len(line)}, expected {width}")
        for ch in line:
            if ch not in ALLOWED:
                raise ValueError(f"unknown symbol {ch!r} in row {index}")

    starts = _locate(lines, START)
    goals = _locate(lines, GOAL)
    if len(starts) != 1:
        raise ValueError(f"expected exactly one start, found {len(starts)}")
    if len(goals) != 1:
        raise ValueError(f"expected exactly one goal, found {len(goals)}")
    return Maze(lines, starts[0], goals[0])
