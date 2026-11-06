"""HTTP-facing wrapper around the rate limiter."""

import math
from dataclasses import dataclass, field


@dataclass
class Response:
    """Minimal response object returned to the web layer."""

    status: int
    headers: dict = field(default_factory=dict)


class Gateway:
    """Applies rate limiting to incoming requests."""

    def __init__(self, limiter):
        self.limiter = limiter

    def handle(self, user_id, endpoint, now):
        """Return 200 with the remaining quota, or 429 with ``Retry-After``."""
        decision = self.limiter.check(user_id, endpoint, now)
        if decision.allowed:
            return Response(200, {"X-RateLimit-Remaining": str(decision.remaining)})
        wait = math.ceil(decision.retry_after)
        return Response(429, {"Retry-After": str(wait)})
