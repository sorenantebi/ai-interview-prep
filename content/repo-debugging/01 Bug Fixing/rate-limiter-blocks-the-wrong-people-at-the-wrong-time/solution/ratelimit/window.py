"""A sliding window of request timestamps."""

from collections import deque


class SlidingWindow:
    """Remembers the timestamps of recent hits.

    At time ``now`` the window covers the half-open interval
    ``(now - size, now]``: a hit made exactly ``size`` seconds ago has
    already left the window.
    """

    def __init__(self, size):
        self.size = size
        self._hits = deque()

    def prune(self, now):
        """Drop hits that are no longer inside the window."""
        cutoff = now - self.size
        while self._hits and self._hits[0] <= cutoff:
            self._hits.popleft()

    def count(self, now):
        """Number of hits inside the window at ``now``."""
        self.prune(now)
        return len(self._hits)

    def record(self, now):
        """Add a hit at ``now``. Timestamps must be non-decreasing."""
        self._hits.append(now)

    def oldest(self):
        """Timestamp of the oldest remembered hit, or ``None`` if empty."""
        return self._hits[0] if self._hits else None
