"""High-level client for the card gateway."""

import itertools
import time
from dataclasses import dataclass

from .errors import InvalidRequestError
from .policy import RetryPolicy
from .retry import call_with_retry


@dataclass(frozen=True)
class Charge:
    """A charge as reported by the gateway."""

    id: str
    amount_cents: int
    currency: str
    status: str

    @classmethod
    def from_response(cls, data):
        return cls(
            id=data["id"],
            amount_cents=data["amount"],
            currency=data["currency"],
            status=data["status"],
        )


class PaymentsClient:
    """Creates charges through a transport, retrying transient failures.

    ``transport`` needs a ``post(path, payload)`` method that returns the
    decoded JSON response or raises a ``PaymentError``.
    """

    def __init__(self, transport, policy=None, sleep=time.sleep):
        self._transport = transport
        self._policy = policy if policy is not None else RetryPolicy()
        self._sleep = sleep
        self._keys = itertools.count(1)

    def charge(self, amount_cents, currency, card_token, idempotency_key=None):
        """Charge ``card_token`` and return a ``Charge``.

        The same idempotency key is sent on every retry so the gateway can
        de-duplicate the request.
        """
        if amount_cents <= 0:
            raise InvalidRequestError("amount must be positive")
        if idempotency_key is None:
            idempotency_key = f"auto-{next(self._keys)}"
        payload = {
            "amount": amount_cents,
            "currency": currency.upper(),
            "source": card_token,
            "idempotency_key": idempotency_key,
        }
        response = call_with_retry(
            lambda: self._transport.post("/charges", payload),
            policy=self._policy,
            sleep=self._sleep,
        )
        return Charge.from_response(response)
