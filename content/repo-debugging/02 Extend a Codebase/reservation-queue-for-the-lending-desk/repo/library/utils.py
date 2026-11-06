"""Time helpers and policy constants."""
from datetime import datetime, timedelta
from typing import Optional

LOAN_DAYS = 14
HOLD_DAYS = 3


class Clock:
    """A controllable clock shared by the service and the tests."""

    def __init__(self, start: Optional[datetime] = None):
        self._now = start if start is not None else datetime(2024, 1, 1, 9, 0)

    def now(self) -> datetime:
        return self._now

    def advance(self, days: int = 0, hours: int = 0) -> None:
        self._now = self._now + timedelta(days=days, hours=hours)


def add_days(moment: datetime, days: int) -> datetime:
    """Return ``moment`` shifted forward by a whole number of days."""
    return moment + timedelta(days=days)
