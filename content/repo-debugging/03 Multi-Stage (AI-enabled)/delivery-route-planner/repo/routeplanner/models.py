"""Plain data objects shared across the package."""

from dataclasses import dataclass

from .units import travel_minutes


@dataclass(frozen=True)
class Road:
    """A directed road segment between two depots."""

    origin: str
    destination: str
    length_km: float
    speed_kmh: float
    closed: bool = False

    def __post_init__(self):
        if self.length_km < 0:
            raise ValueError("road length cannot be negative")
        if self.speed_kmh <= 0:
            raise ValueError("road speed must be positive")

    @property
    def minutes(self):
        """Travel time along this road in minutes."""
        return travel_minutes(self.length_km, self.speed_kmh)


@dataclass(frozen=True)
class Route:
    """A planned route: total travel time and the depots visited in order."""

    minutes: float
    path: tuple
