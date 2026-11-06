"""The inventory service: product registry and stock reservations."""

from typing import Dict, List

from .errors import (
    InsufficientStockError,
    ReservationNotFoundError,
    UnknownProductError,
)
from .models import Product, Reservation
from .utils import normalize_sku, validate_quantity


class InventoryService:
    """Keeps track of products and the units reserved for open orders."""

    def __init__(self) -> None:
        self._products: Dict[str, Product] = {}
        self._reservations: Dict[int, Reservation] = {}
        self._next_reservation_id = 1

    def add_product(self, sku: str, name: str, on_hand: int = 0) -> Product:
        """Register a new product with an initial stock level."""
        key = normalize_sku(sku)
        if key in self._products:
            raise ValueError(f"product {key} already exists")
        if on_hand < 0:
            raise ValueError("on_hand must not be negative")
        product = Product(sku=key, name=name, on_hand=on_hand)
        self._products[key] = product
        return product

    def get(self, sku: str) -> Product:
        """Look up a product by SKU."""
        key = normalize_sku(sku)
        try:
            return self._products[key]
        except KeyError:
            raise UnknownProductError(key) from None

    def products(self) -> List[Product]:
        """All products, ordered by SKU."""
        return [self._products[key] for key in sorted(self._products)]

    def available(self, sku: str) -> int:
        """Units of ``sku`` that can still be reserved."""
        return self.get(sku).available

    def reserve(self, sku: str, quantity: int) -> Reservation:
        """Hold ``quantity`` units for an order.

        Raises ``InsufficientStockError`` if fewer units are available.
        """
        quantity = validate_quantity(quantity)
        product = self.get(sku)
        if quantity > product.available:
            raise InsufficientStockError(
                f"{product.sku}: wanted {quantity}, available {product.available}"
            )
        product.reserved += quantity
        reservation = Reservation(
            id=self._next_reservation_id, sku=product.sku, quantity=quantity
        )
        self._next_reservation_id += 1
        self._reservations[reservation.id] = reservation
        return reservation

    def release(self, reservation_id: int) -> None:
        """Cancel a reservation and make its units available again."""
        reservation = self._close(reservation_id)
        self.get(reservation.sku).reserved -= reservation.quantity

    def commit(self, reservation_id: int) -> None:
        """Ship a reservation: the units leave the warehouse."""
        reservation = self._close(reservation_id)
        product = self.get(reservation.sku)
        product.on_hand -= reservation.quantity
        product.reserved -= reservation.quantity

    def restock(self, sku: str, quantity: int) -> Product:
        """Record a delivery of ``quantity`` units."""
        quantity = validate_quantity(quantity)
        product = self.get(sku)
        product.restock(quantity)
        return product

    def _close(self, reservation_id: int) -> Reservation:
        try:
            return self._reservations.pop(reservation_id)
        except KeyError:
            raise ReservationNotFoundError(reservation_id) from None
