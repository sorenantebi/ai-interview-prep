"""Plain data objects and exceptions used across the pricing package."""

from dataclasses import dataclass
from datetime import date
from typing import Optional


class UnknownProduct(KeyError):
    """Raised when a SKU is not in the catalog."""


class UnknownCurrency(KeyError):
    """Raised when a product has no price in the requested currency."""


class UnknownCoupon(KeyError):
    """Raised when a coupon code is not recognised."""


@dataclass(frozen=True)
class Product:
    """A sellable product with one list price per currency (minor units)."""

    sku: str
    name: str
    prices: dict


@dataclass(frozen=True)
class Sale:
    """A percentage sale on a set of SKUs, valid from start to end inclusive."""

    name: str
    percent: int
    skus: frozenset
    start: date
    end: date


@dataclass(frozen=True)
class Coupon:
    """A percentage coupon that customers enter at checkout."""

    code: str
    percent: int


@dataclass(frozen=True)
class Quote:
    """The result of pricing a line item. All amounts are in minor units."""

    sku: str
    currency: str
    quantity: int
    list_unit_price: int
    sale_unit_price: int
    total: int
    sale_name: Optional[str] = None
    coupon_code: Optional[str] = None
