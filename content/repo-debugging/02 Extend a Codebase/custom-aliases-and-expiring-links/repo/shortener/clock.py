"""Clocks that can be injected into the service.

The service only ever calls ``clock.now()``, which returns seconds since the
epoch as a float. This keeps time-dependent behaviour easy to test.
"""

import time


class SystemClock:
    """Wall-clock time."""

    def now(self):
        return time.time()


class FakeClock:
    """A manually driven clock for tests."""

    def __init__(self, start=1_700_000_000.0):
        self._now = float(start)

    def now(self):
        return self._now

    def advance(self, seconds):
        """Move the clock forward by ``seconds`` (never backwards)."""
        if seconds < 0:
            raise ValueError("clock cannot move backwards")
        self._now += seconds
