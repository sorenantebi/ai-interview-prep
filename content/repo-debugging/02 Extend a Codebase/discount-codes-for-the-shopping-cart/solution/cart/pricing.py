"""Turns a cart into a priced quote."""

from dataclasses import dataclass

from cart.discounts import CART_WIDE


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
    lines = cart.lines()
    nets = {item.sku: item.gross_cents for item in lines}
    deducted = {item.sku: 0 for item in lines}
    # Line-level discounts first, cart-wide ones then work on the reduced amounts.
    ordered = sorted(cart.discounts, key=lambda d: isinstance(d, CART_WIDE))
    for discount in ordered:
        for sku, cents in discount.amounts(lines, nets).items():
            nets[sku] -= cents
            deducted[sku] += cents
    priced = []
    for item in lines:
        net = nets[item.sku]
        tax = tax_table.tax_for(item.product.category, net)
        priced.append(LinePrice(item.sku, item.gross_cents, deducted[item.sku], net, tax))
    return build_quote(priced)


def build_quote(priced: list) -> Quote:
    """Aggregate priced lines into a quote."""
    subtotal = sum(line.gross_cents for line in priced)
    discount = sum(line.discount_cents for line in priced)
    tax = sum(line.tax_cents for line in priced)
    return Quote(priced, subtotal, discount, tax, subtotal - discount + tax)
