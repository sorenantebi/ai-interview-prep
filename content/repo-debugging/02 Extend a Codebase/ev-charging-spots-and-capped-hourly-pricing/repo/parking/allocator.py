"""Decides which spot a vehicle gets."""

from typing import Iterable, Optional, Tuple

from .models import Spot, SpotType, Vehicle, VehicleType

# Spot types a vehicle may use, smallest suitable type first.
_PREFERENCES = {
    VehicleType.MOTORCYCLE: (
        SpotType.MOTORCYCLE,
        SpotType.COMPACT,
        SpotType.REGULAR,
        SpotType.LARGE,
    ),
    VehicleType.CAR: (SpotType.COMPACT, SpotType.REGULAR, SpotType.LARGE),
    VehicleType.VAN: (SpotType.LARGE,),
}


def preferred_spot_types(vehicle: Vehicle) -> Tuple[SpotType, ...]:
    """Return the acceptable spot types for ``vehicle`` in order of preference."""
    return _PREFERENCES[vehicle.vehicle_type]


def find_spot(spots: Iterable[Spot], vehicle: Vehicle) -> Optional[Spot]:
    """Return the best free spot for ``vehicle`` or None if there is none."""
    free = [spot for spot in spots if spot.is_free]
    for spot_type in preferred_spot_types(vehicle):
        for spot in free:
            if spot.spot_type == spot_type:
                return spot
    return None
