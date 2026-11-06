"""Tools for loading ASCII mazes and solving them.

Mazes may contain keys (``a``-``f``) and doors (``A``-``F``).
"""

from .models import Maze
from .parser import parse_grid
from .solver import shortest_path

__all__ = ["Maze", "parse_grid", "shortest_path"]
