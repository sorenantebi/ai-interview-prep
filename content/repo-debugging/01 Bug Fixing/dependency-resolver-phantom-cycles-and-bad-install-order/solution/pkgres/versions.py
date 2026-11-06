"""Version parsing and constraint matching."""

import operator

_OPERATORS = ("==", ">=", "<=", ">", "<")

_COMPARATORS = {
    "==": operator.eq,
    ">=": operator.ge,
    "<=": operator.le,
    ">": operator.gt,
    "<": operator.lt,
}


def parse_version(text):
    """Turn a dotted version such as ``"1.10.2"`` into a comparable tuple.

    Trailing zero components are dropped so that ``"1.0.0"`` and ``"1"``
    compare equal. Raises ``ValueError`` for anything that is not a dotted
    sequence of non-negative integers.
    """
    pieces = text.strip().split(".")
    if not all(piece.isdigit() for piece in pieces):
        raise ValueError(f"invalid version: {text!r}")
    while len(pieces) > 1 and int(pieces[-1]) == 0:
        pieces.pop()
    return tuple(int(piece) for piece in pieces)


def split_clause(clause):
    """Split ``">=1.2"`` into ``(">=", "1.2")``."""
    clause = clause.strip()
    for op in _OPERATORS:
        if clause.startswith(op):
            return op, clause[len(op):].strip()
    raise ValueError(f"invalid version constraint: {clause!r}")


def satisfies(version, spec):
    """Return True if ``version`` meets every comma-separated clause in ``spec``.

    An empty spec accepts any version.
    """
    for clause in spec.split(","):
        if not clause.strip():
            continue
        op, target = split_clause(clause)
        if not _COMPARATORS[op](parse_version(version), parse_version(target)):
            return False
    return True
