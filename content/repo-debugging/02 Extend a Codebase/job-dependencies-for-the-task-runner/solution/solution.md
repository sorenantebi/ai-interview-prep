# Job dependencies for the task runner - Solution

## Root causes / approach
This is a feature request, so there is no bug. The design extends the existing pieces instead of adding new layers.

**Model (`models.py`).** `Job` gets a `depends_on: Tuple[str, ...] = ()` field (default keeps old call sites working). `JobStatus` gets `SKIPPED = "skipped"`; `format_result` already prints `status.value`, so reports show skipped jobs with no change. `RunReport` gets a `skipped` property built on the existing `_names_with` helper. `ok` already means "every result succeeded", so it stays correct.

**Errors (`errors.py`).** New `CycleError(TaskRunnerError)` that stores `cycle` and builds the message `dependency cycle: a -> b -> a` from it.

**Ordering (`registry.py`).** `execution_order()` is the one place that decides the order, so the topological sort lives there.
- It uses Kahn's algorithm with a min-heap keyed on insertion index. That gives exactly the required rule: among ready jobs, the one added first goes first. Jobs without dependencies come out in insertion order, as before.
- Duplicate entries in `depends_on` are collapsed with `dict.fromkeys`, so the pending counters match the number of distinct edges. Unknown dependency names raise `UnknownJobError` here, which is why forward references work (validation happens when the order is requested, not in `add`).
- It is iterative, so a chain of 5000 jobs does not hit the recursion limit. A recursive DFS would fail the long-chain hidden test.
- Cycle: if fewer jobs were scheduled than registered, the unscheduled ones are the cycles plus everything downstream of them. Reporting all of them is wrong (downstream jobs are not part of a cycle). Each unresolved job has at least one unresolved dependency, so walking "first unresolved dependency" from any unresolved job must revisit a node; the part of the path from the revisited node onward is a real cycle. It is rotated to start at the earliest-added member and closed by repeating the first name. This also handles self-dependencies (`['a', 'a']`).
- Complexity: O((V + E) log V) for ordering, O(V) for cycle extraction.

**Skipping (`runner.py`).** `run()` walks `execution_order()`; because the order is topological, the status of every dependency is already known. It keeps a `name -> status` dict, and if any dependency is not `SUCCESS` the job gets a `SKIPPED` result (`attempts=0`, error naming the first non-successful dependency in `depends_on` order) without calling `run_job`. Because skipped is "not success", skipping propagates transitively through indirect dependents. Unrelated jobs run as before. `add()` takes `depends_on` and normalises it to a tuple (a bare string is treated as one name). Since `execution_order()` raises before the loop starts, a cycle or unknown dependency means no job runs.

## How to find it
1. Read `tests/test_dependencies.py` first; the failing tests list the three behaviours: ordering, cycle error, skipping.
2. Open `registry.py`: `execution_order()` currently returns insertion order and is the natural hook. `runner.run()` already calls it, so ordering and cycle errors need no changes in the runner loop.
3. Check the constraints before coding: the tie-break rule (`a(dep d), b, c, d` gives `b, c, d, a`), the cycle shape (closed, rotated, no downstream jobs), and the deep-chain note in the task, which rules out recursive DFS.
4. Add `depends_on` to `Job` and `TaskRunner.add`, `SKIPPED` to `JobStatus`, and `CycleError`; implement the sort, then the skip logic in `run()`.
5. Test by hand with a self-dependency, two disjoint cycles, a job hanging off a cycle, and a 5000-job chain.
