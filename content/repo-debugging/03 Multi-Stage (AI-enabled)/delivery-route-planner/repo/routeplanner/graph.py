"""Road network storage and construction."""

from .models import Road
from .units import KM_PER_MILE

_KM_UNITS = {"km", "kilometer", "kilometers", "kilometre", "kilometres"}
_MILE_UNITS = {"mi", "mile", "miles"}


class RoadGraph:
    """Adjacency-list graph of depots connected by directed roads."""

    def __init__(self):
        self._roads = {}

    def add_depot(self, name):
        """Register a depot, even if no road touches it yet."""
        self._roads.setdefault(name, [])

    def add_road(self, road, two_way=True):
        """Add ``road``; when ``two_way`` also add the reverse direction."""
        self.add_depot(road.origin)
        self.add_depot(road.destination)
        self._roads[road.origin].append(road)
        if two_way:
            self._roads[road.destination].append(
                Road(
                    road.destination,
                    road.origin,
                    road.length_km,
                    road.speed_kmh,
                    road.closed,
                )
            )

    def has_depot(self, name):
        return name in self._roads

    def depots(self):
        """Sorted list of all depot names."""
        return sorted(self._roads)

    def roads_from(self, name):
        """Roads leaving ``name`` (the internal list, do not modify it)."""
        return self._roads[name]

    def road_count(self):
        """Number of directed roads in the graph."""
        return sum(len(roads) for roads in self._roads.values())


def _to_km(distance, unit):
    unit = unit.strip().lower()
    if unit in _KM_UNITS:
        return distance
    if unit in _MILE_UNITS:
        return distance / KM_PER_MILE
    raise ValueError(f"unknown distance unit: {unit!r}")


def build_graph(rows):
    """Build a :class:`RoadGraph` from rows produced by ``parse_roads``."""
    graph = RoadGraph()
    for row in rows:
        road = Road(
            origin=row["origin"],
            destination=row["destination"],
            length_km=_to_km(row["distance"], row.get("unit", "km")),
            speed_kmh=row["speed_kmh"],
            closed=row.get("closed", False),
        )
        graph.add_road(road, two_way=not row.get("one_way", False))
    return graph
