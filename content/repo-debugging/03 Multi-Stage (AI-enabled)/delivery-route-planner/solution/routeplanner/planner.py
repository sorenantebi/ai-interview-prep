"""Delivery planning on top of a :class:`RoadGraph`."""

import heapq

from .graph import RoadGraph
from .models import Route


class NoRouteError(Exception):
    """Raised when no open route connects two depots."""


class UnknownDepotError(KeyError):
    """Raised when a depot name is not part of the graph."""


def _trace(previous, start, goal):
    """Rebuild the depot sequence from the predecessor map (iteratively)."""
    path = [goal]
    while path[-1] != start:
        path.append(previous[path[-1]])
    path.reverse()
    return tuple(path)


def shortest_route(graph, start, goal):
    """Return the fastest :class:`Route` from ``start`` to ``goal``.

    The cost of a road is ``road.minutes``. Roads with ``closed`` set must not
    be used. Roads are directed: only roads leaving a depot may be followed.

    - If ``start == goal`` the route is ``Route(0.0, (start,))``.
    - If either depot is not in the graph, raise ``UnknownDepotError``.
    - If no open route exists, raise ``NoRouteError``.
    - If several routes are equally fast, any of them may be returned.
    """
    for name in (start, goal):
        if not graph.has_depot(name):
            raise UnknownDepotError(name)

    best = {start: 0.0}
    previous = {}
    settled = set()
    heap = [(0.0, start)]

    while heap:
        minutes, depot = heapq.heappop(heap)
        if depot in settled:
            continue  # stale entry, a faster one was already processed
        if depot == goal:
            return Route(minutes, _trace(previous, start, goal))
        settled.add(depot)
        for road in graph.roads_from(depot):
            if road.closed:
                continue
            candidate = minutes + road.minutes
            if candidate < best.get(road.destination, float("inf")):
                best[road.destination] = candidate
                previous[road.destination] = depot
                heapq.heappush(heap, (candidate, road.destination))

    raise NoRouteError(f"no open route from {start!r} to {goal!r}")


def shortest_delivery_time(graph, start, goal):
    """Minutes needed for the fastest route from ``start`` to ``goal``."""
    return shortest_route(graph, start, goal).minutes
