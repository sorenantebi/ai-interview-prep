"""Numeric helpers for latency statistics."""

import math


def mean(values):
    """Arithmetic mean of a non-empty sequence of numbers."""
    values = list(values)
    if not values:
        raise ValueError("mean() requires at least one value")
    return sum(values) / len(values)


def percentile(values, pct):
    """Nearest-rank percentile of a non-empty sequence.

    The value at 1-based rank ``ceil(pct / 100 * n)`` of the sorted data is
    returned; ``pct=0`` yields the minimum. The input is not modified.
    """
    if not 0 <= pct <= 100:
        raise ValueError("pct must be between 0 and 100")
    ordered = sorted(values)
    if not ordered:
        raise ValueError("percentile() requires at least one value")
    rank = max(1, math.ceil(pct * len(ordered) / 100))
    return ordered[rank - 1]
