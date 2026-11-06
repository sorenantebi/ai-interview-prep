"""Data containers used across the package."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Sale:
    """A single line of the sales export."""

    region: str
    rep: str
    amount: float
