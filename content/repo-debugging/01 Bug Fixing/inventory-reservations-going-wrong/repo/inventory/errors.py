"""Exception types raised by the inventory service."""


class InventoryError(Exception):
    """Base class for all inventory errors."""


class UnknownProductError(InventoryError):
    """Raised when a SKU is not known to the service."""


class InsufficientStockError(InventoryError):
    """Raised when a reservation asks for more units than are available."""


class ReservationNotFoundError(InventoryError):
    """Raised when a reservation id does not exist (or was already closed)."""
