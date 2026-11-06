"""Load a :class:`SocialGraph` from edge-list text."""

from typing import Iterable

from .graph import SocialGraph
from .utils import parse_edge_line


def load_edges(lines: Iterable[str]) -> SocialGraph:
    """Build a graph from edge-list lines.

    Every ``"a b"`` line declares that users ``a`` and ``b`` are friends.
    Blank lines, ``#`` comments and self-references (``"7 7"``) are ignored.
    Malformed lines raise ``ValueError`` mentioning the 1-based line number.
    """
    graph = SocialGraph()
    for lineno, line in enumerate(lines, start=1):
        try:
            pair = parse_edge_line(line)
        except ValueError as exc:
            raise ValueError(f"line {lineno}: {exc}") from None
        if pair is None:
            continue
        a, b = pair
        if a == b:
            continue
        graph.add_edge(a, b)
    return graph


def load_file(path: str) -> SocialGraph:
    """Load an edge-list file from disk."""
    with open(path, encoding="utf-8") as handle:
        return load_edges(handle)
