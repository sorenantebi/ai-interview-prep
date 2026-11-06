from payments.backoff import compute_delay
from payments.client import Charge, PaymentsClient
from payments.errors import (
    CardDeclinedError,
    GatewayTimeout,
    InvalidRequestError,
    RateLimitError,
    RetryExhaustedError,
    TransientError,
)
from payments.policy import RetryPolicy
from payments.retry import call_with_retry

OK = {"id": "ch_9", "amount": 250, "currency": "USD", "status": "succeeded"}


class Flaky:
    def __init__(self, *outcomes):
        self.outcomes = list(outcomes)
        self.calls = 0

    def __call__(self):
        self.calls += 1
        outcome = self.outcomes.pop(0)
        if isinstance(outcome, Exception):
            raise outcome
        return outcome


class ScriptedTransport:
    def __init__(self, *responses):
        self.responses = list(responses)
        self.requests = []

    def post(self, path, payload):
        self.requests.append((path, dict(payload)))
        response = self.responses.pop(0)
        if isinstance(response, Exception):
            raise response
        return response


def expect_raises(exc_type, func, *args, **kwargs):
    try:
        func(*args, **kwargs)
    except exc_type as exc:
        return exc
    raise AssertionError(f"expected {exc_type.__name__}")


def test_delay_sequence_with_factor_three():
    delays = [compute_delay(n, 0.5, 3.0, 100.0) for n in range(1, 5)]
    assert delays == [0.5, 1.5, 4.5, 13.5], delays


def test_delay_sequence_with_fractional_factor():
    delays = [compute_delay(n, 1.0, 1.5, 100.0) for n in range(1, 4)]
    assert delays == [1.0, 1.5, 2.25], delays


def test_delay_cap_applies_midway():
    delays = [compute_delay(n, 1.0, 2.0, 5.0) for n in range(1, 6)]
    assert delays == [1.0, 2.0, 4.0, 5.0, 5.0], delays


def test_factor_one_keeps_delay_constant():
    assert [compute_delay(n, 2.0, 1.0, 10.0) for n in (1, 2, 3)] == [2.0] * 3


def test_delay_rejects_retry_number_zero():
    expect_raises(ValueError, compute_delay, 0, 0.5, 2.0, 10.0)


def test_single_attempt_policy_makes_one_call():
    flaky = Flaky(GatewayTimeout("x"), "ok")
    sleeps = []
    exc = expect_raises(
        RetryExhaustedError,
        call_with_retry,
        flaky,
        RetryPolicy(max_attempts=1),
        sleep=sleeps.append,
    )
    assert flaky.calls == 1
    assert sleeps == []
    assert exc.attempts == 1


def test_default_policy_schedule_and_call_count():
    flaky = Flaky(*[GatewayTimeout("x")] * 10)
    sleeps = []
    expect_raises(RetryExhaustedError, call_with_retry, flaky, sleep=sleeps.append)
    assert flaky.calls == 4, flaky.calls
    assert sleeps == [0.5, 1.0, 2.0], sleeps


def test_five_attempts_sleep_four_times():
    flaky = Flaky(*[GatewayTimeout("x")] * 10)
    sleeps = []
    expect_raises(
        RetryExhaustedError,
        call_with_retry,
        flaky,
        RetryPolicy(max_attempts=5),
        sleep=sleeps.append,
    )
    assert sleeps == [0.5, 1.0, 2.0, 4.0], sleeps


def test_sleep_delays_are_capped_by_policy():
    flaky = Flaky(*[GatewayTimeout("x")] * 10)
    sleeps = []
    policy = RetryPolicy(max_attempts=6, base_delay=1.0, factor=2.0, max_delay=3.0)
    expect_raises(RetryExhaustedError, call_with_retry, flaky, policy, sleeps.append)
    assert sleeps == [1.0, 2.0, 3.0, 3.0, 3.0], sleeps


def test_exhausted_error_carries_last_error():
    last = GatewayTimeout("final")
    flaky = Flaky(GatewayTimeout("first"), last)
    exc = expect_raises(
        RetryExhaustedError,
        call_with_retry,
        flaky,
        RetryPolicy(max_attempts=2),
        sleep=lambda s: None,
    )
    assert exc.last_error is last
    assert exc.__cause__ is last


def test_non_retryable_error_is_the_same_instance():
    declined = CardDeclinedError("stolen card")
    caught = expect_raises(
        CardDeclinedError, call_with_retry, Flaky(declined), sleep=lambda s: None
    )
    assert caught is declined


def test_invalid_request_is_not_retried():
    flaky = Flaky(InvalidRequestError("bad currency"), "ok")
    expect_raises(InvalidRequestError, call_with_retry, flaky, sleep=lambda s: None)
    assert flaky.calls == 1


def test_non_payment_errors_propagate_without_retry():
    flaky = Flaky(ValueError("bug in caller"), "ok")
    sleeps = []
    expect_raises(ValueError, call_with_retry, flaky, sleep=sleeps.append)
    assert flaky.calls == 1
    assert sleeps == []


def test_small_rate_limit_hint_does_not_shorten_backoff():
    flaky = Flaky(GatewayTimeout("a"), RateLimitError(retry_after=0.1), "ok")
    sleeps = []
    call_with_retry(flaky, sleep=sleeps.append)
    assert sleeps == [0.5, 1.0], sleeps


def test_rate_limit_without_hint_uses_backoff():
    flaky = Flaky(RateLimitError(), "ok")
    sleeps = []
    call_with_retry(flaky, sleep=sleeps.append)
    assert sleeps == [0.5], sleeps


def test_on_retry_receives_exception_and_delay():
    err = GatewayTimeout("a")
    events = []
    call_with_retry(
        Flaky(err, "ok"),
        sleep=lambda s: None,
        on_retry=lambda attempt, exc, delay: events.append((attempt, exc, delay)),
    )
    assert events == [(1, err, 0.5)], events


def test_should_retry_boundaries():
    policy = RetryPolicy(max_attempts=3)
    assert policy.should_retry(1, TransientError("x"))
    assert policy.should_retry(2, TransientError("x"))
    assert not policy.should_retry(3, TransientError("x"))
    assert not policy.should_retry(1, CardDeclinedError("x"))


def test_policy_validation():
    expect_raises(ValueError, RetryPolicy, max_attempts=0)
    expect_raises(ValueError, RetryPolicy, base_delay=-1.0)
    expect_raises(ValueError, RetryPolicy, factor=0.5)


def test_client_recovers_after_two_timeouts():
    transport = ScriptedTransport(GatewayTimeout("a"), GatewayTimeout("b"), OK)
    sleeps = []
    client = PaymentsClient(transport, sleep=sleeps.append)
    charge = client.charge(250, "usd", "tok_visa", idempotency_key="order-77")
    assert charge == Charge("ch_9", 250, "USD", "succeeded")
    assert sleeps == [0.5, 1.0], sleeps
    assert {p["idempotency_key"] for _, p in transport.requests} == {"order-77"}


def test_client_makes_exactly_default_attempts_then_gives_up():
    transport = ScriptedTransport(*[GatewayTimeout("down")] * 10)
    client = PaymentsClient(transport, sleep=lambda s: None)
    exc = expect_raises(RetryExhaustedError, client.charge, 250, "USD", "tok")
    assert len(transport.requests) == 4, len(transport.requests)
    assert exc.attempts == 4


def test_client_does_not_swallow_invalid_request():
    transport = ScriptedTransport(InvalidRequestError("unknown token"))
    client = PaymentsClient(transport, sleep=lambda s: None)
    expect_raises(InvalidRequestError, client.charge, 250, "USD", "tok_nope")
    assert len(transport.requests) == 1
