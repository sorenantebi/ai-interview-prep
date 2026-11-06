"""Generic retry helper used by the payments client."""

import logging
import time

from .errors import PaymentError, RetryExhaustedError, is_retryable
from .policy import RetryPolicy

logger = logging.getLogger(__name__)

DEFAULT_POLICY = RetryPolicy()


def _next_delay(policy, retry_number, exc):
    """Backoff delay, stretched to the gateway's ``retry_after`` hint if any."""
    delay = policy.delay_for(retry_number)
    hint = getattr(exc, "retry_after", None)
    if hint is not None:
        delay = max(delay, hint)
    return delay


def call_with_retry(func, policy=None, sleep=time.sleep, on_retry=None):
    """Call ``func()`` until it succeeds or the policy says to stop.

    ``sleep`` is injectable so tests do not have to wait. ``on_retry`` is
    called as ``on_retry(attempts_made, exc, delay)`` just before sleeping.

    Raises ``RetryExhaustedError`` when a retryable error outlives the policy.
    """
    if policy is None:
        policy = DEFAULT_POLICY
    attempts = 0
    while True:
        attempts += 1
        try:
            return func()
        except PaymentError as exc:
            if not policy.should_retry(attempts, exc):
                if is_retryable(exc):
                    raise RetryExhaustedError(attempts, exc) from exc
                logger.warning("not retrying %s: %s", type(exc).__name__, exc)
                return None
            delay = _next_delay(policy, attempts, exc)
            if on_retry is not None:
                on_retry(attempts, exc, delay)
            sleep(delay)
