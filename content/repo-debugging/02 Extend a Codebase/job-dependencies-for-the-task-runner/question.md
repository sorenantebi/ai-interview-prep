---
difficulty: Hard
kind: extend
---
# Job dependencies for the task runner

**Kind:** Extend the codebase · **Difficulty:** Hard

## Scenario
`taskrunner` is a small in-process runner used by our build tooling. Today it executes registered jobs strictly in insertion order, so teams have to register jobs in exactly the right sequence by hand, and one failing job does not stop jobs that clearly cannot succeed without it. You are asked to add job dependencies, with a valid execution order, clear cycle errors, and skipping of jobs whose dependencies failed.

## Your tasks
1. **Dependencies and ordering.** `TaskRunner.add(name, func, retries=0, depends_on=())` should accept the names of jobs that must finish successfully first. Dependencies may refer to jobs that are added later. `JobRegistry.execution_order()` must return a valid order (every job after all of its dependencies). Among the jobs that are ready at any point (all their dependencies already scheduled), the one that was **added first** goes first. A dependency that names a job that was never added raises the existing `UnknownJobError` when the order is computed. Jobs without dependencies must behave exactly as before.
2. **Cycle detection.** If the dependencies contain a cycle, computing the order (and therefore `run()`) must raise a new `CycleError` (in `taskrunner/errors.py`, a subclass of `TaskRunnerError`) before any job runs.
   - `error.cycle` is a list of job names that starts and ends with the same name. Each name depends on the one that follows it, and the list starts with the earliest-added job that is part of the cycle.
   - The message reads `dependency cycle: a -> b -> c -> a`.
   - Jobs that merely depend on a cycle, without being part of it, must not appear in the reported cycle. A job that depends on itself is a cycle too.
3. **Skipping dependents of failed jobs.** If a job fails (after its retries), every job that depends on it, directly or indirectly, must not be called. Such a job gets a result with status `JobStatus.SKIPPED` (value `"skipped"`), `attempts == 0`, and an `error` text that names the first dependency (in its `depends_on` order) that did not succeed. Jobs that are unrelated to the failure still run normally. `RunReport` gets a `skipped` property (list of names) next to `succeeded` and `failed`.

## Notes
- Entry points: `TaskRunner` in `taskrunner/runner.py`, the ordering in `taskrunner/registry.py`, data classes in `taskrunner/models.py`. Reuse them; keep the public API that already exists.
- `Job` should expose the dependencies as a `depends_on` tuple of names.
- The existing tests in `tests/test_runner.py` pass today and must keep passing. The failing tests in `tests/test_dependencies.py` describe the new behaviour.
- Real pipelines can have thousands of jobs in a long chain, so avoid solutions that break on deep dependency chains.
- Python 3 standard library only.
- Run runs the tests in `tests/`; Submit runs them plus hidden tests. You may use the AI assistant panel like you would in an AI-enabled interview: it can read every file but can't edit them.
