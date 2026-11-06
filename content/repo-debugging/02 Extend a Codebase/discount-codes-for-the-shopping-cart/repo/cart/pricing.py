"""Turns a cart into a priced quote."""

from dataclasses import dataclass


@dataclass(frozen=True)
class LinePrice:
    sku: str
    gross_cents: int
    discount_cents: int
    net_cents: int
    tax_cents: int


@dataclass(frozen=True)
class Quote:
    lines: list
    subtotal_cents: int
    discount_cents: int
    tax_cents: int
    total_cents: int


def price_cart(cart, tax_table) -> Quote:
    """Price every line of the cart and total it up."""
    priced = []
    for item in cart.lines():
        gross = item.gross_cents
        tax = tax_table.tax_for(item.product.category, gross)
        priced.append(LinePrice(item.sku, gross, 0, gross, tax))
    return build_quote(priced)


def build_quote(priced: list) -> Quote:
    """Aggregate priced lines into a quote."""
    subtotal = sum(line.gross_cents for line in priced)
    discount = sum(line.discount_cents for line in priced)
    tax = sum(line.tax_cents for line in priced)
    return Quote(priced, subtotal, discount, tax, subtotal - discount + tax)
