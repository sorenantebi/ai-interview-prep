"""The rate limiter itself."""

from dataclasses import dataclass

from ratelimit.keys import bucket_key
from ratelimit.window import SlidingWindow


@dataclass(frozen=True)
class Decision:
    """Outcome of a single quota check."""

    allowed: bool
    remaining: int
    retry_after: float


class RateLimiter:
    """Enforces a :class:`Policy` per user and endpoint."""

    def __init__(self, policy):
        self.policy = policy
        self._windows = {}

    def _window_for(self, user_id, endpoint):
        key = bucket_key(user_id, endpoint)
        window = self._windows.get(key)
        if window is None:
            window = SlidingWindow(self.policy.window)
            self._windows[key] = window
        return window

    def check(self, user_id, endpoint, now):
        """Count a request and decide whether it may proceed.

        Denied requests are not recorded.
        """
        window = self._window_for(user_id, endpoint)
        limit = self.policy.limit_for(endpoint)
        used = window.count(now)
        if used >= limit:
            retry_after = window.oldest() + window.size - now
            return Decision(False, 0, retry_after)
        window.record(now)
        return Decision(True, limit - used - 1, 0.0)

    def usage(self, user_id, endpoint, now):
        """Hits currently counted for this user on this endpoint."""
        return self._window_for(user_id, endpoint).count(now)

    def reset(self, user_id, endpoint):
        """Forget all hits for one user on one endpoint."""
        self._windows.pop(bucket_key(user_id, endpoint), None)
