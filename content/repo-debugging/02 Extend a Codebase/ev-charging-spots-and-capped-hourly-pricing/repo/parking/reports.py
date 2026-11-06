"""Simple reporting over finished stays."""

from decimal import Decimal
from typing import Dict, Iterable

from .models import Receipt


def revenue_by_type(receipts: Iterable[Receipt]) -> Dict[str, Decimal]:
    """Return the total fees collected, keyed by vehicle type value."""
    totals: Dict[str, Decimal] = {}
    for receipt in receipts:
        key = receipt.ticket.vehicle_type.value
        totals[key] = totals.get(key, Decimal("0")) + receipt.fee
    return totals
