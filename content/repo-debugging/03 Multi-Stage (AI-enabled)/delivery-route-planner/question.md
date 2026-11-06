---
difficulty: Hard
kind: multi-stage
---
# Delivery Route Planner

**Kind:** Multi-stage (AI-enabled round) · **Difficulty:** Hard

## Scenario
`routeplanner` is the small library our dispatch team uses to estimate how long a delivery van needs to get from one depot to another. Road data is imported from CSV files supplied by regional partners. Some partners report distances in kilometres, others in miles. Dispatchers have noticed that the estimated times on some roads look far too optimistic. The core "shortest delivery time" function was never finished, and the network is now growing to tens of thousands of depots.

## Your tasks
1. **Stage 1: fix the bug.** Travel times for roads that come from the partner feeds reporting miles are far too short. Find and fix the cause (the failing graph test shows the symptom).
2. **Stage 2: implement the feature.** `shortest_route` in `routeplanner/planner.py` is a stub. Implement it so it returns the fastest route (total minutes and the ordered depots) between two depots. Closed roads must not be used, one-way roads only work in their own direction, and the error cases described in the docstring must be handled.
3. **Stage 3: make it fast.** The planner will be queried on networks with tens of thousands of depots and a few hundred thousand directed roads. Hidden tests assert that a query finishes in well under a second on such a network. Make sure your implementation scales.

## Notes
- Entry points: `routeplanner.loader.parse_roads` (CSV text to rows), `routeplanner.graph.build_graph` (rows to a `RoadGraph`), and `routeplanner.planner.shortest_route` / `shortest_delivery_time`.
- Times are in minutes. A road's travel time is its length in kilometres divided by its speed in km/h, times 60.
- Only the Python standard library is available.
- Run runs the tests in `tests/`; Submit runs them plus hidden tests. You may use the AI assistant panel like you would in an AI-enabled interview: it can read every file but can't edit them.
