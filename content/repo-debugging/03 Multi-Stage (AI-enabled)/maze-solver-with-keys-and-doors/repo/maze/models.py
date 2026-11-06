"""Data model for a maze loaded from an ASCII grid."""

from typing import Iterator, Sequence, Tuple

Cell = Tuple[int, int]

WALL = "#"
OPEN = "."
START = "S"
GOAL = "G"

_STEPS = ((-1, 0), (1, 0), (0, -1), (0, 1))


class Maze:
    """A rectangular maze.

    ``grid`` is a sequence of equally long strings. ``start`` and ``goal``
    are ``(row, col)`` positions inside it.
    """

    def __init__(self, grid: Sequence[str], start: Cell, goal: Cell) -> None:
        self.grid = list(grid)
        self.rows = len(self.grid)
        self.cols = len(self.grid[0]) if self.grid else 0
        self.start = start
        self.goal = goal

    def in_bounds(self, pos: Cell) -> bool:
        """Return True if ``pos`` lies inside the grid."""
        row, col = pos
        return 0 <= row < self.rows and 0 <= col < self.cols

    def cell(self, pos: Cell) -> str:
        """Return the symbol at ``pos``."""
        row, col = pos
        return self.grid[row][col]

    def is_wall(self, pos: Cell) -> bool:
        """Return True if ``pos`` is a wall."""
        return self.cell(pos) == WALL

    def neighbors(self, pos: Cell) -> Iterator[Cell]:
        """Yield the walkable cells next to ``pos``.

        Order is up, down, left, right. Doors are not treated specially;
        callers decide whether they can be entered.
        """
        row, col = pos
        for d_row, d_col in _STEPS:
            r, c = row + d_row, col + d_col
            if 0 <= r < self.rows and 0 <= c < self.cols and self.grid[r][c] != WALL:
                yield (r, c)
