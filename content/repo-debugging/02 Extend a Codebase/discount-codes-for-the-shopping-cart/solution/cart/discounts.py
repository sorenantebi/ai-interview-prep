"""Discount codes that can be attached to a cart.

A discount does not modify the cart. Given the cart's lines and the net
amount (in cents) each line currently costs, it reports how many cents to
take off every line, so tax can later be computed on what is really paid.
"""

from dataclasses import dataclass

from cart.utils import round_div, split_proportionally


class DiscountError(Exception):
    """A code is unknown or cannot be combined with the codes already on the cart."""


@dataclass(frozen=True)
class Discount:
    """Base class for all discount codes."""

    code: str

    def amounts(self, lines, nets):
        """Return ``{sku: cents_to_deduct}``.

        ``lines`` is the list of ``LineItem`` objects in the cart and ``nets``
        maps each sku to the cents that line costs after earlier discounts.
        Never deduct more than a line's net amount.
        """
        raise NotImplementedError


@dataclass(frozen=True)
class PercentOff(Discount):
    """Take ``percent`` percent off every line."""

    percent: int

    def amounts(self, lines, nets):
        return {sku: round_div(net * self.percent, 100) for sku, net in nets.items()}


@dataclass(frozen=True)
class FixedOff(Discount):
    """Take ``cents`` off the whole cart."""

    cents: int

    def amounts(self, lines, nets):
        skus = sorted(nets)
        total = min(self.cents, sum(nets.values()))
        shares = split_proportionally(total, [nets[sku] for sku in skus])
        return dict(zip(skus, shares))


@dataclass(frozen=True)
class BuyOneGetOne(Discount):
    """Every second unit of ``sku`` is free."""

    sku: str

    def amounts(self, lines, nets):
        for line in lines:
            if line.sku == self.sku:
                return {line.sku: (line.quantity // 2) * line.unit_price_cents}
        return {}


CART_WIDE = (PercentOff, FixedOff)
