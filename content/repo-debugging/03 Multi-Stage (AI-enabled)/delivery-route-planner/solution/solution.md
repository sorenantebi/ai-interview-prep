# Delivery Route Planner - Solution

## Root causes / approach

**Stage 1: `routeplanner/graph.py`, `_to_km`.** For rows whose unit is miles the builder divided the distance by `KM_PER_MILE` instead of multiplying by it. That is the km-to-miles direction, so a 10 mi road became about 6.2 km instead of 16.1 km. Every road from a miles-based feed was about 2.6 times too short, which made travel times look far too optimistic. Kilometre rows were unaffected, which is why only the miles test failed. The fix is `distance * KM_PER_MILE`.

**Stage 2: `routeplanner/planner.py`, `shortest_route`.** This is Dijkstra's algorithm over `RoadGraph`, using the existing pieces: `graph.has_depot` for validation, `graph.roads_from` for adjacency, `Road.closed` to skip closed roads and `Road.minutes` as the non-negative edge weight. A `best` dict holds the best known time per depot, and a `previous` dict holds the predecessor of each depot. When the goal is popped from the queue its time is final, and the path is rebuilt iteratively from `previous` (no recursion, so long routes are safe). Unknown depots raise `UnknownDepotError` before any search. An exhausted queue raises `NoRouteError`. `start == goal` falls out naturally: the start is popped first with 0.0 minutes and a path of one depot. `shortest_delivery_time` just reads `.minutes`.

**Stage 3: heap instead of a linear scan.** The first version most people write keeps a dict of tentative distances and uses `min(...)` over it to choose the next depot. That costs O(V) per step, so O(V^2 + E) overall. With 25,000 depots and a frontier of thousands of depots this takes many seconds. Replacing the scan with a `heapq` priority queue gives O((V + E) log V). Instead of a decrease-key operation, each improvement pushes a new `(minutes, depot)` entry, and stale entries are skipped on pop with the `settled` set. The planner stops as soon as the goal is popped, so queries do not always touch the whole network. The hidden large-input tests finish in roughly 0.1 s per query with this approach.

## How to find it

- Start with `tests/test_graph.py::test_mile_rows_are_converted_to_km`. It fails with a length of about 6.2 where 16.09 is expected. It is the only failing test that does not depend on the stub, so the bug is in the code that handles miles. Follow `build_graph` into `_to_km` and compare the formula with the helpers in `units.py` (`miles_to_km` multiplies, `km_to_miles` divides).
- Then run `tests/test_planner.py`. All planner tests fail with `NotImplementedError`, which points at the stub. Read its docstring: it lists the closed-road, same-depot and error rules to implement. `test_mile_road_travel_time` only passes once stage 1 is fixed as well.
- For stage 3, build a graph of tens of thousands of depots and time a query. If the time grows quadratically with the number of depots (double the size, roughly four times the time), look for the linear `min(...)` scan. Switch to a heap and skip stale entries.
