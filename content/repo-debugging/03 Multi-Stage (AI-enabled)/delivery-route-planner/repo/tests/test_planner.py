from routeplanner.graph import build_graph
from routeplanner.planner import (
    NoRouteError,
    shortest_delivery_time,
    shortest_route,
)


def _row(origin, destination, distance, unit="km", speed=60.0, **extra):
    row = {
        "origin": origin,
        "destination": destination,
        "distance": distance,
        "unit": unit,
        "speed_kmh": speed,
    }
    row.update(extra)
    return row


def _network(closed_bc=False):
    return build_graph(
        [
            _row("A", "B", 60.0),
            _row("B", "C", 30.0, closed=closed_bc),
            _row("A", "C", 120.0),
            _row("C", "D", 10.0, speed=30.0),
        ]
    )


def test_shortest_time_prefers_two_hop_route():
    minutes = shortest_delivery_time(_network(), "A", "C")
    assert abs(minutes - 90.0) < 1e-6, minutes


def test_route_returns_path_and_total():
    route = shortest_route(_network(), "A", "D")
    assert route.path == ("A", "B", "C", "D")
    assert abs(route.minutes - 110.0) < 1e-6, route.minutes


def test_closed_road_is_skipped():
    route = shortest_route(_network(closed_bc=True), "A", "C")
    assert route.path == ("A", "C")
    assert abs(route.minutes - 120.0) < 1e-6


def test_mile_road_travel_time():
    graph = build_graph([_row("A", "B", 50.0, unit="mi", speed=80.0)])
    minutes = shortest_delivery_time(graph, "A", "B")
    assert abs(minutes - 60.3504) < 1e-4, minutes


def test_no_route_raises():
    graph = _network()
    graph.add_depot("Z")
    try:
        shortest_delivery_time(graph, "A", "Z")
    except NoRouteError:
        pass
    else:
        assert False, "expected NoRouteError"


def test_same_depot_is_free():
    route = shortest_route(_network(), "A", "A")
    assert route.minutes == 0.0
    assert route.path == ("A",)
