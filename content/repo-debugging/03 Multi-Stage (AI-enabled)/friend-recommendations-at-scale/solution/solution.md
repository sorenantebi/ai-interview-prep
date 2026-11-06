# Friend recommendations at scale - Solution

## Root causes / approach

**Stage 1 - `friends/loader.py`, `load_edges`.** The loader called `graph.add_edge(a, b)`, which records only a one-way link `a -> b` (it registers `b` as a user but does not add `a` to `b`'s adjacency set). So for every line `"a b"`, `b` appeared in `a`'s friend list but not the other way round. Users that only ever appeared as the second id existed in the graph with zero friends. The fix is to call `graph.add_friendship(a, b)`, which adds both directions. Self-loops are already skipped before that call, so its `ValueError` is never hit.

**Stage 2 - `friends/recommender.py`, `recommend_friends`.** Candidates are friends-of-friends. For each friend `f` of the user, walk `f`'s neighbours and count how often each candidate appears. That count is exactly the number of mutual friends. Skip the user and anyone already in the user's friend set. Candidates with no mutual friend never enter the counter, which matches the spec. Rank by `(-count, id)`. Validate the user first (`KeyError`), then handle `k <= 0`. The code uses `graph.neighbors` (live set, no copy) and never mutates the graph.

**Stage 3 - performance.** The naive version loops over all `N` users and intersects friend sets, costing `O(N * avg_degree)` per query. That is about 10^5 set intersections (plus a copy each if `friends_of` is used) per call, which is seconds over a few hundred queries. The counting approach costs `O(sum of degrees of the user's friends)`, which is tiny for ordinary users and about the size of a popular friend's list in the worst case. Selecting the top `k` with `heapq.nsmallest` on key `(-count, id)` costs `O(C log k)` for `C` candidates instead of sorting all of them (`nsmallest` falls back to a full sort when `k` is large). Using `neighbors` instead of `friends_of` avoids copying a popular user's 5000-element set on every query.

## How to find it

1. Run the tests. `test_load_makes_friendship_visible_from_both_sides` and `test_load_degrees_are_symmetric` fail while the direct `SocialGraph.add_friendship` tests pass, so the graph class is fine and the loader is the suspect.
2. Print `g.friends_of(2)` after `load_edges(["1 2"])`: it is empty while `friends_of(1)` is `{2}`. Read `load_edges` and then the docstrings in `graph.py`: `add_edge` is documented as one-way and `add_friendship` as mutual.
3. For stage 2, read the docstring of the stub and the `Recommendation` tuple. Sketch the friends-of-friends counting on the example graph in `tests/test_recommender.py` before writing code (user 1: candidate 5 has three mutual friends, 6 has two, 7 has one).
4. For stage 3, ask what the loop iterates over. If it is "all users", it scales with the whole graph. Iterating only over the neighbourhood of the user's friends scales with the local structure. Then check the hub and star cases: very popular users make friend lists large, so avoid per-call copies and full sorts.
