"""Small parsing helpers shared by the loaders."""

from typing import Optional, Tuple

COMMENT_PREFIX = "#"


def parse_edge_line(line: str) -> Optional[Tuple[int, int]]:
    """Parse a line of the form ``"<a> <b>"`` into a pair of ints.

    Returns ``None`` for blank lines and comment lines (starting with ``#``).
    Raises ``ValueError`` if the line does not contain exactly two integer ids.
    """
    text = line.strip()
    if not text or text.startswith(COMMENT_PREFIX):
        return None
    parts = text.split()
    if len(parts) != 2:
        raise ValueError(f"expected two user ids, got {text!r}")
    return int(parts[0]), int(parts[1])
