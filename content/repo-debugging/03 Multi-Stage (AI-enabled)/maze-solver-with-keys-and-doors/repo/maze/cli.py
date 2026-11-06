"""Command line entry point: ``python -m maze.cli [file]``."""

import sys
from typing import List, Optional

from .parser import parse_grid
from .render import format_solution
from .solver import shortest_path


def solve_text(text: str) -> str:
    """Parse ``text``, solve it and return the formatted solution."""
    maze = parse_grid(text)
    return format_solution(maze, shortest_path(maze))


def main(argv: Optional[List[str]] = None) -> int:
    """Read a maze from the file in ``argv`` (or stdin) and print the solution."""
    args = sys.argv[1:] if argv is None else argv
    if args:
        with open(args[0], encoding="utf-8") as handle:
            text = handle.read()
    else:
        text = sys.stdin.read()
    print(solve_text(text))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
