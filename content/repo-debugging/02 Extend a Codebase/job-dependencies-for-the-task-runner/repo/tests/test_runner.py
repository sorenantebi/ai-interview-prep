from taskrunner.errors import DuplicateJobError
from taskrunner.models import JobStatus
from taskrunner.registry import JobRegistry
from taskrunner.runner import TaskRunner
from taskrunner.utils import format_report


def test_runs_jobs_in_insertion_order():
    log = []
    runner = TaskRunner()
    for name in ["c", "a", "b"]:
        runner.add(name, lambda n=name: log.append(n))
    runner.run()
    assert log == ["c", "a", "b"]


def test_collects_return_values():
    runner = TaskRunner()
    runner.add("one", lambda: 1)
    runner.add("two", lambda: 2)
    report = runner.run()
    assert report.get("one").value == 1
    assert report.get("two").value == 2
    assert report.succeeded == ["one", "two"]
    assert report.ok


def test_failure_is_recorded_and_later_jobs_still_run():
    def boom():
        raise ValueError("boom")

    runner = TaskRunner()
    runner.add("bad", boom)
    runner.add("good", lambda: "fine")
    report = runner.run()
    assert report.get("bad").status is JobStatus.FAILED
    assert report.get("bad").error == "ValueError: boom"
    assert report.get("good").status is JobStatus.SUCCESS
    assert report.failed == ["bad"]
    assert not report.ok


def test_retries_until_success():
    calls = []

    def flaky():
        calls.append(1)
        if len(calls) < 3:
            raise RuntimeError("not yet")
        return "done"

    runner = TaskRunner()
    runner.add("flaky", flaky, retries=2)
    result = runner.run().get("flaky")
    assert result.status is JobStatus.SUCCESS
    assert result.attempts == 3
    assert result.value == "done"


def test_duplicate_name_rejected():
    runner = TaskRunner()
    runner.add("a", lambda: None)
    try:
        runner.add("a", lambda: None)
    except DuplicateJobError:
        pass
    else:
        assert False, "expected DuplicateJobError"


def test_shared_empty_registry_is_used():
    registry = JobRegistry()
    runner = TaskRunner(registry)
    runner.add("a", lambda: None)
    assert len(registry) == 1
    assert runner.registry is registry


def test_format_report():
    def boom():
        raise KeyError("x")

    runner = TaskRunner()
    runner.add("a", lambda: 1)
    runner.add("b", boom, retries=1)
    text = format_report(runner.run())
    lines = text.split("\n")
    assert lines[0] == "a: success"
    assert lines[1].startswith("b: failed (attempts: 2)")
