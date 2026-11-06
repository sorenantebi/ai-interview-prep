"""Helpers for the day-first date strings used throughout the package."""

from datetime import date


def parse_date(text):
    """Parse a 'D/M/YYYY' string into a ``datetime.date``.

    Zero padding is optional ('05/03/2025' and '5/3/2025' are the same day).
    Raises ``ValueError`` for malformed or impossible dates.
    """
    parts = text.strip().split("/")
    if len(parts) != 3:
        raise ValueError(f"expected D/M/YYYY, got {text!r}")
    day, month, year = (int(part) for part in parts)
    return date(year, month, day)


def format_date(value):
    """Format a ``datetime.date`` as an unpadded 'D/M/YYYY' string."""
    return f"{value.day}/{value.month}/{value.year}"
