"""The parking lot: parks vehicles, issues tickets and takes payment."""

from datetime import datetime
from typing import Dict

from .allocator import find_spot
from .models import Receipt, Spot, SpotType, Ticket, Vehicle
from .pricing import calculate_fee

SPOT_PREFIX = {
    SpotType.MOTORCYCLE: "M",
    SpotType.COMPACT: "C",
    SpotType.REGULAR: "R",
    SpotType.LARGE: "L",
    SpotType.EV: "E",
}


class LotFullError(Exception):
    """Raised when no suitable spot is free for an arriving vehicle."""


class ParkingLot:
    """A lot built from a layout such as ``{SpotType.COMPACT: 10}``."""

    def __init__(self, layout: Dict[SpotType, int]):
        self._spots: Dict[str, Spot] = {}
        for spot_type, count in layout.items():
            prefix = SPOT_PREFIX[spot_type]
            for number in range(1, count + 1):
                spot_id = f"{prefix}{number}"
                self._spots[spot_id] = Spot(spot_id, spot_type)
        self._tickets: Dict[int, Ticket] = {}
        self._next_ticket_id = 1

    def park(self, vehicle: Vehicle, now: datetime) -> Ticket:
        """Park ``vehicle`` and return its ticket."""
        if any(t.plate == vehicle.plate for t in self._tickets.values()):
            raise ValueError(f"vehicle {vehicle.plate} is already parked")
        spot = find_spot(self._spots.values(), vehicle)
        if spot is None:
            raise LotFullError(f"no free spot for {vehicle.plate}")
        spot.plate = vehicle.plate
        ticket = Ticket(
            ticket_id=self._next_ticket_id,
            plate=vehicle.plate,
            vehicle_type=vehicle.vehicle_type,
            spot_id=spot.spot_id,
            entry_time=now,
        )
        self._tickets[ticket.ticket_id] = ticket
        self._next_ticket_id += 1
        return ticket

    def leave(self, ticket_id: int, now: datetime) -> Receipt:
        """Release the spot of ``ticket_id`` and return the receipt."""
        ticket = self._tickets.pop(ticket_id, None)
        if ticket is None:
            raise KeyError(f"unknown ticket {ticket_id}")
        self._spots[ticket.spot_id].plate = None
        fee = calculate_fee(ticket.entry_time, now, ticket.vehicle_type)
        return Receipt(ticket=ticket, exit_time=now, fee=fee)

    def available(self) -> Dict[str, int]:
        """Return the number of free spots per spot type value."""
        counts = {spot_type.value: 0 for spot_type in SpotType}
        for spot in self._spots.values():
            if spot.is_free:
                counts[spot.spot_type.value] += 1
        return counts
