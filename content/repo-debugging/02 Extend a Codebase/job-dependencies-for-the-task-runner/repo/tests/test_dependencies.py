from taskrunner.models import JobStatus
from taskrunner.runner import TaskRunner


def _recorder(log, name, value=None):
    def job():
        log.append(name)
        return value

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


def test_dependency_runs_before_dependent():
    log = []
    runner = TaskRunner()
    runner.add("package", _recorder(log, "package"), depends_on=["compile"])
    runner.add("compile", _recorder(log, "compile"))
    runner.run()
    assert log == ["compile", "package"]


def test_ready_jobs_keep_insertion_order():
    runner = TaskRunner()
    runner.add("a", lambda: None, depends_on=["d"])
    runner.add("b", lambda: None)
    runner.add("c", lambda: None)
    runner.add("d", lambda: None)
    assert _order(runner) == ["b", "c", "d", "a"]


def test_diamond_dependencies():
    runner = TaskRunner()
    runner.add("deploy", lambda: None, depends_on=["build", "test"])
    runner.add("test", lambda: None, depends_on=["build"])
    runner.add("build", lambda: None)
    assert _order(runner) == ["build", "test", "deploy"]


def test_cycle_error_names_the_cycle():
    runner = TaskRunner()
    runner.add("a", lambda: None, depends_on=["b"])
    runner.add("b", lambda: None, depends_on=["c"])
    runner.add("c", lambda: None, depends_on=["a"])
    exc = _expect_cycle(runner)
    assert exc.cycle == ["a", "b", "c", "a"]
    assert "dependency cycle: a -> b -> c -> a" in str(exc)


def test_cycle_excludes_jobs_that_only_depend_on_it():
    runner = TaskRunner()
    runner.add("x", lambda: None, depends_on=["a"])
    runner.add("a", lambda: None, depends_on=["b"])
    runner.add("b", lambda: None, depends_on=["a"])
    exc = _expect_cycle(runner)
    assert exc.cycle == ["a", "b", "a"]


def test_cycle_prevents_any_job_from_running():
    log = []
    runner = TaskRunner()
    runner.add("free", _recorder(log, "free"))
    runner.add("p", _recorder(log, "p"), depends_on=["q"])
    runner.add("q", _recorder(log, "q"), depends_on=["p"])
    _expect_cycle(runner)
    assert log == []


def test_failed_job_skips_dependents():
    log = []
    runner = TaskRunner()
    runner.add("fetch", _failing(log, "fetch"))
    runner.add("parse", _recorder(log, "parse"), depends_on=["fetch"])
    runner.add("publish", _recorder(log, "publish"), depends_on=["parse"])
    runner.add("lint", _recorder(log, "lint"))
    report = runner.run()
    assert log == ["fetch", "lint"]
    assert report.get("fetch").status is JobStatus.FAILED
    assert report.get("parse").status is JobStatus.SKIPPED
    assert report.get("publish").status is JobStatus.SKIPPED
    assert report.get("lint").status is JobStatus.SUCCESS
    assert report.get("parse").attempts == 0
    assert "fetch" in report.get("parse").error
    assert "parse" in report.get("publish").error
    assert "fetch" not in report.get("publish").error


def test_report_lists_skipped_jobs():
    runner = TaskRunner()
    runner.add("fetch", _failing([], "fetch"))
    runner.add("parse", lambda: None, depends_on=["fetch"])
    runner.add("lint", lambda: None)
    report = runner.run()
    assert report.skipped == ["parse"]
    assert report.failed == ["fetch"]
    assert report.succeeded == ["lint"]
    assert not report.ok
