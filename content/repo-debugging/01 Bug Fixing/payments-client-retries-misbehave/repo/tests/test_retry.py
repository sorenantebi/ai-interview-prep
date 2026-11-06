from payments.errors import (
    CardDeclinedError,
    GatewayTimeout,
    RateLimitError,
    RetryExhaustedError,
)
from payments.policy import RetryPolicy
from payments.retry import call_with_retry


class Flaky:
    """Callable that returns or raises the queued outcomes in order."""

    def __init__(self, *outcomes):
        self.outcomes = list(outcomes)
        self.calls = 0

    def __call__(self):
        self.calls += 1
        outcome = self.outcomes.pop(0)
        if isinstance(outcome, Exception):
            raise outcome
        return outcome


def expect_raises(exc_type, func, *args, **kwargs):
    try:
        func(*args, **kwargs)
    except exc_type as exc:
        return exc
    raise AssertionError(f"expected {exc_type.__name__}")


def test_returns_result_without_sleeping():
    sleeps = []
    assert call_with_retry(Flaky("ok"), sleep=sleeps.append) == "ok"
    assert sleeps == []


def test_retries_transient_errors_with_growing_delay():
    flaky = Flaky(GatewayTimeout("t1"), GatewayTimeout("t2"), "ok")
    sleeps = []
    policy = RetryPolicy(max_attempts=4, base_delay=0.5, factor=2.0)
    assert call_with_retry(flaky, policy, sleep=sleeps.append) == "ok"
    assert sleeps == [0.5, 1.0], sleeps


def test_gives_up_after_max_attempts():
    flaky = Flaky(*[GatewayTimeout("down")] * 10)
    exc = expect_raises(
        RetryExhaustedError,
        call_with_retry,
        flaky,
        RetryPolicy(max_attempts=3),
        sleep=lambda s: None,
    )
    assert flaky.calls == 3, f"made {flaky.calls} calls"
    assert exc.attempts == 3


def test_non_retryable_error_is_raised_immediately():
    flaky = Flaky(CardDeclinedError("insufficient funds"), "ok")
    sleeps = []
    expect_raises(CardDeclinedError, call_with_retry, flaky, sleep=sleeps.append)
    assert flaky.calls == 1
    assert sleeps == []


def test_retry_after_hint_stretches_the_wait():
    flaky = Flaky(RateLimitError(retry_after=7.0), "ok")
    sleeps = []
    call_with_retry(flaky, sleep=sleeps.append)
    assert sleeps == [7.0], sleeps


def test_on_retry_callback_sees_each_failed_attempt():
    flaky = Flaky(GatewayTimeout("a"), GatewayTimeout("b"), "ok")
    seen = []
    call_with_retry(
        flaky,
        sleep=lambda s: None,
        on_retry=lambda attempt, exc, delay: seen.append(attempt),
    )
    assert seen == [1, 2]
