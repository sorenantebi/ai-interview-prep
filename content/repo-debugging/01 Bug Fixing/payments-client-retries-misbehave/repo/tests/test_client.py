from payments.client import Charge, PaymentsClient
from payments.errors import (
    CardDeclinedError,
    GatewayTimeout,
    InvalidRequestError,
    RetryExhaustedError,
)
from payments.policy import RetryPolicy

OK = {"id": "ch_1", "amount": 1500, "currency": "EUR", "status": "succeeded"}


class ScriptedTransport:
    """Fake transport that replays queued responses and records requests."""

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


def test_charge_returns_charge():
    client = PaymentsClient(ScriptedTransport(OK), sleep=lambda s: None)
    charge = client.charge(1500, "eur", "tok_visa")
    assert charge == Charge("ch_1", 1500, "EUR", "succeeded")


def test_retries_reuse_the_idempotency_key():
    transport = ScriptedTransport(GatewayTimeout("slow"), OK)
    client = PaymentsClient(transport, sleep=lambda s: None)
    client.charge(1500, "EUR", "tok_visa")
    keys = [payload["idempotency_key"] for _, payload in transport.requests]
    assert len(keys) == 2
    assert keys[0] == keys[1]


def test_declined_card_reaches_the_caller():
    transport = ScriptedTransport(CardDeclinedError("do not honor"))
    client = PaymentsClient(transport, sleep=lambda s: None)
    expect_raises(CardDeclinedError, client.charge, 1500, "EUR", "tok_bad")
    assert len(transport.requests) == 1


def test_client_stops_after_policy_max_attempts():
    transport = ScriptedTransport(*[GatewayTimeout("down")] * 10)
    client = PaymentsClient(
        transport, policy=RetryPolicy(max_attempts=3), sleep=lambda s: None
    )
    expect_raises(RetryExhaustedError, client.charge, 1500, "EUR", "tok_visa")
    assert len(transport.requests) == 3, len(transport.requests)


def test_rejects_non_positive_amount_without_calling_gateway():
    transport = ScriptedTransport(OK)
    client = PaymentsClient(transport, sleep=lambda s: None)
    expect_raises(InvalidRequestError, client.charge, 0, "EUR", "tok_visa")
    assert transport.requests == []
