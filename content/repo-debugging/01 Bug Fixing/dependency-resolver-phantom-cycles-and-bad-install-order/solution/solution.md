# Dependency resolver: phantom cycles and bad install order - Solution

## Root causes / approach

**1. `pkgres/resolver.py`, `Resolver._visit`: "visited" used as "on the current path".**
The method raised `CycleError` whenever a package was already in `state.visited`. `visited` contains every package ever entered, including those whose dependencies are completely processed. A package reached a second time through a different parent (a diamond, a root that is also a dependency, or a root listed twice) was therefore reported as a cycle. A real cycle exists only when the package is on the current DFS stack. The fix is to check `state.stack` first and raise `CycleError(state.stack[start:] + [name])`, which also trims the chain to the cycle itself (the old chain included the unrelated packages above the cycle). After that, a package already in `visited` simply returns, since it and its dependencies are already in `order`. The version check stays before both checks, so a second parent with a stricter constraint still gets a `VersionConflict`.

**2. `pkgres/planner.py`, `build_plan`: stage level computed with `min` instead of `max`.**
A package's stage must be one later than its latest dependency. Using `min` of the dependency levels places a package right after its shallowest dependency. When a package has dependencies at different depths (`app` needs `lib`, which needs `core`, and also needs `tool`), `app` lands in the same stage as `lib`. Because names inside a stage are sorted, `app` can then be installed before `lib`. The fix is `1 + max(dep_levels)`. The bug is hidden behind bug 1 for diamond-shaped inputs, because those fail with the false cycle first, but `test_package_follows_its_deepest_dependency` has no shared dependency and fails on its own.

**3. `pkgres/versions.py`, `parse_version`: components kept as strings.**
`tuple(pieces)` returns a tuple of strings, so `("1", "10") < ("1", "9")` is true and `>=1.9` rejects `1.10.0`. The trailing-zero loop converts to `int` for the comparison only, which hides the issue. The fix is `tuple(int(piece) for piece in pieces)`.

Complexity is linear in packages plus dependency edges for the resolver and the planner (apart from the per-stage sort).

## How to find it
- Start with `test_diamond_is_not_a_cycle` in `tests/test_resolver.py`: the traceback goes into `Resolver._visit`. The graph has no cycle, but one package is reached twice. Print `state.visited` and `state.stack` at the raise: the package is in `visited` but not in `stack`. That tells you the check is on the wrong set.
- Fix that, re-run, and `test_package_follows_its_deepest_dependency` still fails. Compare the actual stages to the expected ones: `app` is in the same stage as `lib`. Print the `levels` dict in `build_plan` and see that `app` got 1 instead of 2, which points to the `min`.
- `test_numeric_ordering` and `test_two_digit_minor_version_is_accepted` both involve a two-digit component. Print `parse_version("1.10")` and notice the tuple holds strings.
- The hidden tests also check that `CycleError.chain` contains only the cycle, and a random 200-package graph checks the order and the stages against an independent longest-path computation.
