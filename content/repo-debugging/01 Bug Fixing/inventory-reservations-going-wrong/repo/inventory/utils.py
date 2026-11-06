"""Input validation helpers."""


def normalize_sku(sku: str) -> str:
    """Return the canonical form of a SKU (trimmed, upper case)."""
    if not isinstance(sku, str) or not sku.strip():
        raise ValueError("sku must be a non-empty string")
    return sku.strip().upper()


def validate_quantity(quantity: int) -> int:
    """Check that ``quantity`` is a positive integer and return it."""
    if isinstance(quantity, bool) or not isinstance(quantity, int):
        raise ValueError("quantity must be an integer")
    if quantity <= 0:
        raise ValueError("quantity must be positive")
    return quantity
