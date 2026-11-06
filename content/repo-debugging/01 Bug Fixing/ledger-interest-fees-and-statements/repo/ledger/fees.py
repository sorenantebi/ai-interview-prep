"""Fee schedule: wire transfers and overdrafts."""

WIRE_RATE_BPS = 50
WIRE_MIN_CENTS = 100
WIRE_MAX_CENTS = 2_500
OVERDRAFT_FEE_CENTS = 3_500


def wire_fee_cents(amount_cents: int) -> int:
    """Fee for an outgoing wire: 0.50% of the amount, at least $1.00 and
    at most $25.00."""
    if amount_cents <= 0:
        raise ValueError("wire amount must be positive")
    fee = round(amount_cents * WIRE_RATE_BPS / 10_000)
    return max(WIRE_MIN_CENTS, min(WIRE_MAX_CENTS, fee))


def overdraft_fee_cents(balance_cents: int) -> int:
    """Flat fee charged when an account ends the day below zero."""
    if balance_cents < 0:
        return OVERDRAFT_FEE_CENTS
    return 0
