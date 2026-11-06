"""Read-only reports built on top of the inventory service."""

from typing import Dict, List

from .models import Product
from .service import InventoryService


def low_stock(service: InventoryService, threshold: int = 5) -> List[Product]:
    """Products whose available units are at or below ``threshold``.

    The most urgent product (fewest units available) comes first; ties are
    broken by SKU so the picking list is stable.
    """
    low = [p for p in service.products() if p.available <= threshold]
    return sorted(low, key=lambda p: (p.on_hand, p.sku))


def summary(service: InventoryService) -> Dict[str, int]:
    """Aggregate stock figures across all products."""
    products = service.products()
    return {
        "products": len(products),
        "on_hand": sum(p.on_hand for p in products),
        "reserved": sum(p.reserved for p in products),
        "available": sum(p.available for p in products),
    }
