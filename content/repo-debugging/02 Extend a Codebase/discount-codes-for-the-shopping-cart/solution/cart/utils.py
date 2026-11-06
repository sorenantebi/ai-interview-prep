"""Small integer-money helpers shared across the cart package."""


def round_div(numerator: int, denominator: int) -> int:
    """Divide two non-negative integers, rounding halves up."""
    return (2 * numerator + denominator) // (2 * denominator)


def split_proportionally(total: int, weights: list) -> list:
    """Split ``total`` into integer shares proportional to ``weights``.

    The shares always add up to ``total``. Leftover cents go to the entries
    with the largest fractional remainder, earlier entries first on ties.
    If every weight is zero all shares are zero.
    """
    weight_sum = sum(weights)
    if weight_sum == 0:
        return [0] * len(weights)
    shares = [total * w // weight_sum for w in weights]
    remainders = [total * w % weight_sum for w in weights]
    leftover = total - sum(shares)
    order = sorted(range(len(weights)), key=lambda i: (-remainders[i], i))
    for i in order[:leftover]:
        shares[i] += 1
    return shares


def normalize_code(raw: str) -> str:
    """Canonical form of a discount code: trimmed and upper-case."""
    return raw.strip().upper()


def format_cents(cents: int) -> str:
    """Render cents as a decimal string, e.g. ``1999`` -> ``'19.99'``."""
    sign = "-" if cents < 0 else ""
    cents = abs(cents)
    return f"{sign}{cents // 100}.{cents % 100:02d}"
