import heapq
import random
import time

from routeplanner.graph import RoadGraph, build_graph
from routeplanner.models import Road
from routeplanner.planner import (
    NoRouteError,
    UnknownDepotError,
    shortest_delivery_time,
    shortest_route,
)


def _close(a, b, tol=1e-6):
    return abs(a - b) < tol


def _road(a, b, minutes, closed=False):
    """Road that takes exactly ``minutes`` (speed fixed at 60 km/h)."""
    return Road(a, b, float(minutes), 60.0, closed)


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


def _reference_minutes(graph, start, goal):
    best = {start: 0.0}
    heap = [(0.0, start)]
    done = set()
    while heap:
        d, u = heapq.heappop(heap)
        if u in done:
            continue
        if u == goal:
            return d
        done.add(u)
        for r in graph.roads_from(u):
            if r.closed:
                continue
            nd = d + r.minutes
            if nd < best.get(r.destination, float("inf")):
                best[r.destination] = nd
                heapq.heappush(heap, (nd, r.destination))
    return None


_LARGE = {}


def _large_graph():
    if "graph" not in _LARGE:
        rng = random.Random(0)
        n = 25000
        speeds = (40.0, 60.0, 80.0, 100.0)
        graph = RoadGraph()
        for i in range(n - 1):
            graph.add_road(
                Road(f"D{i}", f"D{i + 1}", rng.uniform(1.0, 20.0), rng.choice(speeds))
            )
        for _ in range(2 * n):
            a = rng.randrange(n)
            b = rng.randrange(n)
            if a != b:
                graph.add_road(
                    Road(f"D{a}", f"D{b}", rng.uniform(1.0, 60.0), rng.choice(speeds))
                )
        graph.add_depot("ISOLATED")
        _LARGE["graph"] = graph
    return _LARGE["graph"]


# ---------------------------------------------------------------- stage 1


def test_mixed_units_use_correct_conversion():
    graph = build_graph(
        [
            _row("A", "B", 10.0, unit="mi", speed=100.0),
            _row("A", "B", 20.0, unit="km", speed=100.0),
        ]
    )
    minutes = shortest_delivery_time(graph, "A", "B")
    assert _close(minutes, 9.656064), minutes


def test_unit_aliases_and_case():
    graph = build_graph([_row("A", "B", 1.0, unit="Miles")])
    assert _close(graph.roads_from("A")[0].length_km, 1.609344)
    graph = build_graph([_row("A", "B", 1.0, unit=" MI ")])
    assert _close(graph.roads_from("A")[0].length_km, 1.609344)


def test_unknown_unit_raises():
    try:
        build_graph([_row("A", "B", 1.0, unit="furlong")])
    except ValueError:
        pass
    else:
        assert False, "expected ValueError"


# ---------------------------------------------------------------- stage 2


def test_unknown_depots_raise():
    graph = build_graph([_row("A", "B", 5.0)])
    for start, goal in (("A", "X"), ("X", "A"), ("X", "X")):
        try:
            shortest_route(graph, start, goal)
        except UnknownDepotError:
            pass
        else:
            assert False, f"expected UnknownDepotError for {start}->{goal}"


def test_only_closed_connection_raises_no_route():
    graph = build_graph([_row("A", "B", 5.0, closed=True)])
    try:
        shortest_route(graph, "A", "B")
    except NoRouteError:
        pass
    else:
        assert False, "expected NoRouteError"


def test_one_way_roads_respect_direction():
    graph = build_graph([_row("A", "B", 30.0, one_way=True)])
    assert _close(shortest_delivery_time(graph, "A", "B"), 30.0)
    try:
        shortest_route(graph, "B", "A")
    except NoRouteError:
        pass
    else:
        assert False, "expected NoRouteError"


def test_faster_longer_route_beats_slow_direct_road():
    graph = RoadGraph()
    graph.add_road(Road("A", "B", 100.0, 50.0))
    graph.add_road(Road("A", "C", 60.0, 120.0))
    graph.add_road(Road("C", "B", 60.0, 120.0))
    route = shortest_route(graph, "A", "B")
    assert route.path == ("A", "C", "B")
    assert _close(route.minutes, 60.0)


def test_distance_improves_after_first_discovery():
    graph = RoadGraph()
    graph.add_road(_road("A", "B", 100))
    graph.add_road(_road("A", "C", 10))
    graph.add_road(_road("C", "D", 10))
    graph.add_road(_road("D", "B", 10))
    route = shortest_route(graph, "A", "B")
    assert route.path == ("A", "C", "D", "B")
    assert _close(route.minutes, 30.0)


def test_zero_length_road():
    graph = RoadGraph()
    graph.add_road(Road("A", "B", 0.0, 50.0))
    graph.add_road(_road("B", "C", 7))
    route = shortest_route(graph, "A", "C")
    assert route.path == ("A", "B", "C")
    assert _close(route.minutes, 7.0)


def test_query_does_not_modify_graph_and_is_repeatable():
    graph = RoadGraph()
    graph.add_road(_road("A", "B", 5))
    graph.add_road(_road("B", "C", 5))
    before = (graph.road_count(), graph.depots(), len(graph.roads_from("B")))
    first = shortest_route(graph, "A", "C")
    second = shortest_route(graph, "A", "C")
    after = (graph.road_count(), graph.depots(), len(graph.roads_from("B")))
    assert before == after
    assert first == second


def test_delivery_time_matches_route_minutes():
    graph = RoadGraph()
    graph.add_road(_road("A", "B", 12))
    graph.add_road(_road("B", "C", 8))
    assert _close(
        shortest_delivery_time(graph, "A", "C"), shortest_route(graph, "A", "C").minutes
    )


def test_random_small_graphs_match_reference():
    rng = random.Random(0)
    for _ in range(60):
        n = 25
        graph = RoadGraph()
        for i in range(n):
            graph.add_depot(f"N{i}")
        for _ in range(45):
            a, b = rng.randrange(n), rng.randrange(n)
            if a == b:
                continue
            road = Road(
                f"N{a}",
                f"N{b}",
                rng.uniform(0.0, 40.0),
                rng.choice((30.0, 60.0, 90.0)),
                rng.random() < 0.2,
            )
            graph.add_road(road, two_way=rng.random() < 0.5)
        start, goal = f"N{rng.randrange(n)}", f"N{rng.randrange(n)}"
        expected = _reference_minutes(graph, start, goal)
        if expected is None:
            try:
                shortest_route(graph, start, goal)
            except NoRouteError:
                continue
            assert False, "expected NoRouteError"
        route = shortest_route(graph, start, goal)
        assert _close(route.minutes, expected), (route.minutes, expected)
        assert route.path[0] == start and route.path[-1] == goal


# ---------------------------------------------------------------- stage 3


def test_large_network_is_fast_and_correct():
    graph = _large_graph()
    queries = (("D0", "D24999"), ("D12000", "D3"))
    started = time.perf_counter()
    routes = [shortest_route(graph, s, g) for s, g in queries]
    elapsed = time.perf_counter() - started
    assert elapsed < 1.0, f"two queries took {elapsed:.2f}s"
    for (start, goal), route in zip(queries, routes):
        assert _close(route.minutes, _reference_minutes(graph, start, goal))
        assert route.path[0] == start and route.path[-1] == goal
        for a, b in zip(route.path, route.path[1:]):
            assert any(r.destination == b for r in graph.roads_from(a))


def test_large_network_unreachable_depot_is_fast():
    graph = _large_graph()
    started = time.perf_counter()
    try:
        shortest_route(graph, "D0", "ISOLATED")
    except NoRouteError:
        pass
    else:
        assert False, "expected NoRouteError"
    elapsed = time.perf_counter() - started
    assert elapsed < 1.0, f"query took {elapsed:.2f}s"


def test_long_chain_has_no_recursion_limit_and_is_fast():
    n = 20000
    graph = RoadGraph()
    for i in range(n - 1):
        graph.add_road(_road(f"C{i}", f"C{i + 1}", 2))
    started = time.perf_counter()
    route = shortest_route(graph, "C0", f"C{n - 1}")
    elapsed = time.perf_counter() - started
    assert elapsed < 1.0, f"query took {elapsed:.2f}s"
    assert len(route.path) == n
    assert _close(route.minutes, 2.0 * (n - 1), 1e-3)
