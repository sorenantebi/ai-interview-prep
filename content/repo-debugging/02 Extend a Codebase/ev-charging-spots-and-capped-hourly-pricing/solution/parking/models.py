"""Plain data objects shared across the parking package."""

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional


class VehicleType(Enum):
    MOTORCYCLE = "motorcycle"
    CAR = "car"
    VAN = "van"


class SpotType(Enum):
    MOTORCYCLE = "motorcycle"
    COMPACT = "compact"
    REGULAR = "regular"
    LARGE = "large"
    EV = "ev"


@dataclass(frozen=True)
class Vehicle:
    """A vehicle identified by its licence plate."""

    plate: str
    vehicle_type: VehicleType
    needs_charging: bool = False


@dataclass
class Spot:
    """A single parking spot; ``plate`` is None while the spot is free."""

    spot_id: str
    spot_type: SpotType
    plate: Optional[str] = None

    @property
    def is_free(self) -> bool:
        return self.plate is None


@dataclass(frozen=True)
class Ticket:
    """Issued when a vehicle enters the lot."""

    ticket_id: int
    plate: str
    vehicle_type: VehicleType
    spot_id: str
    entry_time: datetime


@dataclass(frozen=True)
class Receipt:
    """Returned when a vehicle leaves the lot."""

    ticket: Ticket
    exit_time: datetime
    fee: Decimal
