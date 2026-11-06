"""Money helpers. Amounts are always integers in minor units (cents)."""

CURRENCY_SYMBOLS = {"USD": "$", "EUR": "EUR "}


def percent_off(amount, percent):
    """Return ``amount`` reduced by ``percent`` percent.

    The discount itself is rounded half up to a whole minor unit, so
    ``percent_off(5, 50)`` is 2 (a discount of 3).
    """
    if not 0 <= percent <= 100:
        raise ValueError(f"percent must be between 0 and 100, got {percent}")
    discount = (amount * percent + 50) // 100
    return amount - discount


def format_money(amount, currency):
    """Format minor units for display, e.g. ``format_money(1999, "USD")``."""
    major, minor = divmod(amount, 100)
    prefix = CURRENCY_SYMBOLS.get(currency, currency + " ")
    return f"{prefix}{major}.{minor:02d}"
