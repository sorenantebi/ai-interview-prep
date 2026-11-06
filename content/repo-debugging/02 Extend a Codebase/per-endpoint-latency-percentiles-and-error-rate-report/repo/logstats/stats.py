"""Numeric helpers for latency statistics."""


def mean(values):
    """Arithmetic mean of a non-empty sequence of numbers."""
    values = list(values)
    if not values:
        raise ValueError("mean() requires at least one value")
    return sum(values) / len(values)
