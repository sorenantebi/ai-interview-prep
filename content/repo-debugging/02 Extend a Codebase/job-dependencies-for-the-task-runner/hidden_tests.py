import random

from taskrunner.errors import TaskRunnerError, UnknownJobError
from taskrunner.models import JobStatus
from taskrunner.registry import JobRegistry
from taskrunner.runner import TaskRunner
from taskrunner.utils import format_report


def _recorder(log, name):
    def job():
        log.append(name)

    return job


def _failing(log, name):
    def job():
        log.append(name)
        raise RuntimeError(f"{name} exploded")

    return job


def _order(runner):
    return [job.name for job in runner.registry.execution_order()]


def _expect_cycle(runner):
    from taskrunner.errors import CycleError

    try:
        runner.run()
    except CycleError as exc:
        return exc
    assert False, "expected CycleError"


def _assert_valid_cycle(deps, cycle):
    assert len(cycle) >= 2 and cycle[0] == cycle[-1], cycle
    for cur, nxt in zip(cycle, cycle[1:]):
        assert nxt in deps[cur], f"{cur} does not depend on {nxt}"


def test_cycle_error_is_a_task_runner_error():
    from taskrunner.errors import CycleError

    assert issubclass(CycleError, TaskRunnerError)


def test_unknown_dependency_raises_before_running():
    log = []
    runner = TaskRunner()
    runner.add("a", _recorder(log, "a"), depends_on=["ghost"])
    runner.add("b", _recorder(log, "b"))
    try:
        runner.run()
    except UnknownJobError as exc:
        assert "ghost" in str(exc)
    else:
        assert False, "expected UnknownJobError"
    assert log == []


def test_self_dependency_is_a_cycle():
    runner = TaskRunner()
    runner.add("ok", lambda: None)
    runner.add("a", lambda: None, depends_on=["a"])
    exc = _expect_cycle(runner)
    assert exc.cycle == ["a", "a"]
    assert "a -> a" in str(exc)


def test_cycle_starts_at_earliest_added_member():
    runner = TaskRunner()
    runner.add("b", lambda: None, depends_on=["c"])
    runner.add("c", lambda: None, depends_on=["a"])
    runner.add("a", lambda: None, depends_on=["b"])
    exc = _expect_cycle(runner)
    assert exc.cycle == ["b", "c", "a", "b"]
    assert str(exc).endswith("b -> c -> a -> b")


def test_two_disjoint_cycles_report_a_real_cycle():
    deps = {"a": ["b"], "b": ["a"], "c": ["d"], "d": ["c"], "e": ["a"]}
    runner = TaskRunner()
    for name, d in deps.items():
        runner.add(name, lambda: None, depends_on=d)
    exc = _expect_cycle(runner)
    _assert_valid_cycle(deps, exc.cycle)
    assert "e" not in exc.cycle


def test_forward_reference_and_duplicate_entries():
    runner = TaskRunner()
    runner.add("b", lambda: 2, depends_on=["a", "a"])
    runner.add("a", lambda: 1)
    assert _order(runner) == ["a", "b"]
    report = runner.run()
    assert report.succeeded == ["a", "b"]


def test_execution_order_is_repeatable_and_registry_unchanged():
    runner = TaskRunner()
    runner.add("a", lambda: None, depends_on=["b"])
    runner.add("b", lambda: None)
    first = _order(runner)
    second = _order(runner)
    assert first == second == ["b", "a"]
    assert runner.registry.names() == ["a", "b"]


def test_jobs_without_dependencies_unchanged():
    registry = JobRegistry()
    runner = TaskRunner(registry)
    for name in ["z", "y", "x"]:
        runner.add(name, lambda: None)
    assert _order(runner) == ["z", "y", "x"]


def test_long_chain_does_not_blow_the_stack():
    n = 5000
    runner = TaskRunner()
    for i in range(n):
        deps = [f"j{i + 1}"] if i + 1 < n else []
        runner.add(f"j{i}", lambda: None, depends_on=deps)
    assert _order(runner) == [f"j{i}" for i in range(n - 1, -1, -1)]
    report = runner.run()
    assert len(report.succeeded) == n


def test_long_cycle_is_reported_fully():
    n = 3000
    deps = {f"j{i}": [f"j{(i + 1) % n}"] for i in range(n)}
    runner = TaskRunner()
    for name, d in deps.items():
        runner.add(name, lambda: None, depends_on=d)
    exc = _expect_cycle(runner)
    assert len(exc.cycle) == n + 1
    assert exc.cycle[0] == "j0"
    _assert_valid_cycle(deps, exc.cycle)


def test_order_matches_reference_on_random_dag():
    rng = random.Random(0)
    n = 150
    ranks = list(range(n))
    rng.shuffle(ranks)
    names = [f"j{k}" for k in range(n)]
    deps = {}
    for k in range(n):
        lower = [names[m] for m in range(n) if ranks[m] < ranks[k]]
        deps[names[k]] = rng.sample(lower, min(len(lower), rng.randint(0, 3)))
    runner = TaskRunner()
    for name in names:
        runner.add(name, lambda: None, depends_on=deps[name])
    expected = []
    done = set()
    while len(expected) < n:
        for name in names:
            if name not in done and all(d in done for d in deps[name]):
                expected.append(name)
                done.add(name)
                break
    assert _order(runner) == expected


def test_skipped_error_names_the_failing_dependency():
    log = []
    runner = TaskRunner()
    runner.add("good", _recorder(log, "good"))
    runner.add("bad", _failing(log, "bad"))
    runner.add("target", _recorder(log, "target"), depends_on=["good", "bad"])
    report = runner.run()
    result = report.get("target")
    assert result.status is JobStatus.SKIPPED
    assert "bad" in result.error
    assert "good" not in result.error
    assert "target" not in log


def test_first_failing_dependency_in_declared_order_is_named():
    runner = TaskRunner()
    runner.add("x1", _failing([], "x1"))
    runner.add("x2", _failing([], "x2"))
    runner.add("z", lambda: None, depends_on=["x2", "x1"])
    error = runner.run().get("z").error
    assert "x2" in error
    assert "x1" not in error


def test_failure_at_top_of_diamond_skips_both_branches_and_join():
    log = []
    runner = TaskRunner()
    runner.add("top", _failing(log, "top"))
    runner.add("left", _recorder(log, "left"), depends_on=["top"])
    runner.add("right", _recorder(log, "right"), depends_on=["top"])
    runner.add("join", _recorder(log, "join"), depends_on=["left", "right"])
    runner.add("side", _recorder(log, "side"))
    report = runner.run()
    assert log == ["top", "side"]
    assert report.skipped == ["left", "right", "join"]
    assert "left" in report.get("join").error
    assert report.get("side").status is JobStatus.SUCCESS


def test_skipped_job_is_not_retried():
    calls = []
    runner = TaskRunner()
    runner.add("a", _failing(calls, "a"))
    runner.add("b", _failing(calls, "b"), retries=3, depends_on=["a"])
    report = runner.run()
    assert calls == ["a"]
    assert report.get("b").status is JobStatus.SKIPPED
    assert report.get("b").attempts == 0


def test_dependent_runs_when_dependency_succeeds_after_retry():
    state = {"n": 0}

    def flaky():
        state["n"] += 1
        if state["n"] == 1:
            raise RuntimeError("first attempt")
        return "ok"

    log = []
    runner = TaskRunner()
    runner.add("flaky", flaky, retries=1)
    runner.add("after", _recorder(log, "after"), depends_on=["flaky"])
    report = runner.run()
    assert report.get("flaky").attempts == 2
    assert report.get("after").status is JobStatus.SUCCESS
    assert log == ["after"]


def test_report_order_includes_skipped_jobs_in_execution_order():
    runner = TaskRunner()
    runner.add("c", lambda: None, depends_on=["b"])
    runner.add("b", _failing([], "b"), depends_on=["a"])
    runner.add("a", lambda: None)
    report = runner.run()
    assert [r.name for r in report.results] == ["a", "b", "c"]
    assert [r.status for r in report.results] == [
        JobStatus.SUCCESS,
        JobStatus.FAILED,
        JobStatus.SKIPPED,
    ]


def test_format_report_shows_skipped_jobs():
    runner = TaskRunner()
    runner.add("a", _failing([], "a"))
    runner.add("c", lambda: None, depends_on=["a"])
    text = format_report(runner.run())
    lines = text.split("\n")
    assert lines[0].startswith("a: failed")
    assert lines[1].startswith("c: skipped")
