"""Delivery planning on top of a :class:`RoadGraph`."""

from .graph import RoadGraph
from .models import Route


class NoRouteError(Exception):
    """Raised when no open route connects two depots."""


class UnknownDepotError(KeyError):
    """Raised when a depot name is not part of the graph."""


def shortest_route(graph, start, goal):
    """Return the fastest :class:`Route` from ``start`` to ``goal``.

    The cost of a road is ``road.minutes``. Roads with ``closed`` set must not
    be used. Roads are directed: only roads leaving a depot may be followed.

    - If ``start == goal`` the route is ``Route(0.0, (start,))``.
    - If either depot is not in the graph, raise ``UnknownDepotError``.
    - If no open route exists, raise ``NoRouteError``.
    - If several routes are equally fast, any of them may be returned.
    """
    raise NotImplementedError("shortest_route is not implemented yet")


def shortest_delivery_time(graph, start, goal):
    """Minutes needed for the fastest route from ``start`` to ``goal``."""
    return shortest_route(graph, start, goal).minutes
