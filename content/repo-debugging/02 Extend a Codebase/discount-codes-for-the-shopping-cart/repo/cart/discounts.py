"""Discount codes that can be attached to a cart.

A discount does not modify the cart. Given the cart's lines and the net
amount (in cents) each line currently costs, it reports how many cents to
take off every line, so tax can later be computed on what is really paid.
"""

from dataclasses import dataclass


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


@dataclass(frozen=True)
class FixedOff(Discount):
    """Take ``cents`` off the whole cart."""

    cents: int


@dataclass(frozen=True)
class BuyOneGetOne(Discount):
    """Every second unit of ``sku`` is free."""

    sku: str
