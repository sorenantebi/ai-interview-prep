"""Small helpers for working with naive datetimes and calendar days."""

from datetime import date, datetime, time, timedelta


def day_start(day: date) -> datetime:
    """Midnight at the beginning of the given day."""
    return datetime.combine(day, time.min)


def next_midnight(moment: datetime) -> datetime:
    """The midnight that ends the calendar day containing ``moment``."""
    return day_start(moment.date() + timedelta(days=1))


def fits_in_day(start: datetime, end: datetime) -> bool:
    """Return True if an interval stays within the calendar day it starts on.

    Rooms are closed overnight, so bookings must not run past the midnight
    following their start.
    """
    return end <= next_midnight(start)
