"""Fee calculation for finished stays."""

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Dict, Optional

from .models import VehicleType
from .utils import started_hours

DEFAULT_HOURLY_RATE = Decimal("2.00")
HOURS_PER_DAY = 24


@dataclass(frozen=True)
class Tariff:
    """Hourly rate plus the maximum charged for any 24-hour block."""

    hourly_rate: Decimal
    daily_cap: Decimal


TARIFFS: Dict[VehicleType, Tariff] = {
    VehicleType.MOTORCYCLE: Tariff(Decimal("1.00"), Decimal("6.00")),
    VehicleType.CAR: Tariff(Decimal("2.50"), Decimal("15.00")),
    VehicleType.VAN: Tariff(Decimal("4.00"), Decimal("24.00")),
}


def calculate_fee(
    entry_time: datetime,
    exit_time: datetime,
    vehicle_type: Optional[VehicleType] = None,
) -> Decimal:
    """Return the fee for a stay.

    Without a vehicle type a flat rate applies to every started hour. With a
    vehicle type the type's tariff is used: every complete 24 hours cost the
    daily cap and the remaining started hours are capped at the daily cap too.
    """
    hours = started_hours(entry_time, exit_time)
    if vehicle_type is None:
        return DEFAULT_HOURLY_RATE * hours
    tariff = TARIFFS[vehicle_type]
    full_days, remaining_hours = divmod(hours, HOURS_PER_DAY)
    remainder_fee = min(tariff.hourly_rate * remaining_hours, tariff.daily_cap)
    return tariff.daily_cap * full_days + remainder_fee
