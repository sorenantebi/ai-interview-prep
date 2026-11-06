"""Small helpers for reading and printing money values."""


def parse_amount(text):
    """Convert text such as ``'$1,200.50'`` or ``'-15'`` into a float.

    Raises ValueError if the text is empty or not a number.
    """
    cleaned = text.strip().replace("$", "").replace(",", "")
    if not cleaned:
        raise ValueError("empty amount")
    return float(cleaned)


def format_money(value):
    """Format a number with thousands separators and two decimals."""
    return f"{value:,.2f}"
