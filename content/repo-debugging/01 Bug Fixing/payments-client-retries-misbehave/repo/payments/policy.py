"""Retry configuration shared by the payments client."""

from dataclasses import dataclass

from .backoff import compute_delay
from .errors import is_retryable


@dataclass(frozen=True)
class RetryPolicy:
    """How often and how patiently a failed request is sent again.

    ``max_attempts`` counts the first request as well.
    """

    max_attempts: int = 4
    base_delay: float = 0.5
    factor: float = 2.0
    max_delay: float = 10.0

    def __post_init__(self):
        if self.max_attempts < 1:
            raise ValueError("max_attempts must be at least 1")
        if self.base_delay < 0:
            raise ValueError("base_delay must not be negative")
        if self.factor < 1:
            raise ValueError("factor must be at least 1")

    def should_retry(self, attempts_made, exc):
        """True if a request that has failed ``attempts_made`` times so far,
        most recently with ``exc``, should be sent again."""
        if not is_retryable(exc):
            return False
        return attempts_made <= self.max_attempts

    def delay_for(self, retry_number):
        """Seconds to sleep before retry number ``retry_number`` (1-based)."""
        return compute_delay(
            retry_number, self.base_delay, self.factor, self.max_delay
        )
