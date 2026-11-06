"""Data models for the inventory service."""

from dataclasses import dataclass


@dataclass
class Product:
    """A stocked product.

    ``on_hand`` is the number of physical units in the warehouse and
    ``reserved`` is the number of those units promised to open orders.
    """

    sku: str
    name: str
    on_hand: int = 0
    reserved: int = 0

    @property
    def available(self) -> int:
        """Units that can still be promised to new orders."""
        return self.on_hand - self.reserved

    def restock(self, quantity: int) -> None:
        """Add newly delivered units to the shelf."""
        self.on_hand += quantity


@dataclass
class Reservation:
    """A hold on some units of a product for an open order."""

    id: int
    sku: str
    quantity: int
