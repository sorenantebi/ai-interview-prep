"""Exception hierarchy for the payments client."""


class PaymentError(Exception):
    """Base class for every error raised by the payments client."""


class TransientError(PaymentError):
    """A failure that may succeed if the same request is sent again."""


class GatewayTimeout(TransientError):
    """The gateway did not answer in time."""


class RateLimitError(TransientError):
    """The gateway asked us to slow down.

    ``retry_after`` is the number of seconds the gateway wants us to wait,
    or ``None`` if it did not say.
    """

    def __init__(self, message="rate limited", retry_after=None):
        super().__init__(message)
        self.retry_after = retry_after


class CardDeclinedError(PaymentError):
    """The issuer declined the card. Sending the request again will not help."""


class InvalidRequestError(PaymentError):
    """The request was malformed or rejected by validation."""


class RetryExhaustedError(PaymentError):
    """A retryable request kept failing until the policy gave up."""

    def __init__(self, attempts, last_error):
        super().__init__(f"gave up after {attempts} attempts: {last_error}")
        self.attempts = attempts
        self.last_error = last_error


def is_retryable(exc):
    """Return True if ``exc`` describes a failure worth retrying."""
    return isinstance(exc, TransientError)
