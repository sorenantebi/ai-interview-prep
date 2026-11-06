"""Formatting helpers for the catalogue API."""


def format_price(price_cents, currency="EUR"):
    """Render an integer amount of cents as e.g. ``12.50 EUR``."""
    euros, cents = divmod(price_cents, 100)
    return f"{euros}.{cents:02d} {currency}"
