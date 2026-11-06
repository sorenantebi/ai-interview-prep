"""Helpers for working with money stored as integer cents."""


def div_round_half_up(numerator: int, denominator: int) -> int:
    """Divide two integers and round the result half away from zero.

    Only integer arithmetic is used, so there is no floating point error.
    ``denominator`` must be positive.
    """
    if denominator <= 0:
        raise ValueError("denominator must be positive")
    magnitude = (2 * abs(numerator) + denominator) // (2 * denominator)
    return -magnitude if numerator < 0 else magnitude


def format_cents(cents: int) -> str:
    """Render an amount in cents as a dollar string, e.g. ``-$1,234.50``."""
    sign = "-" if cents < 0 else ""
    dollars, remainder = divmod(abs(cents), 100)
    return f"{sign}${dollars:,}.{remainder:02d}"
