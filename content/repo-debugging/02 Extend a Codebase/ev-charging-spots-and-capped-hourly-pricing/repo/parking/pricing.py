"""Fee calculation for finished stays."""

from datetime import datetime
from decimal import Decimal

from .utils import started_hours

DEFAULT_HOURLY_RATE = Decimal("2.00")


def calculate_fee(entry_time: datetime, exit_time: datetime) -> Decimal:
    """Return the fee for a stay: a flat rate for every started hour."""
    return DEFAULT_HOURLY_RATE * started_hours(entry_time, exit_time)
