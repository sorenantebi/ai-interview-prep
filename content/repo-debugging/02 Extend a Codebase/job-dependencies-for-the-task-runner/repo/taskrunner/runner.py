"""The task runner: registers jobs and executes them."""

from typing import Any, Callable, Optional

from taskrunner.models import Job, JobResult, JobStatus, RunReport
from taskrunner.registry import JobRegistry


class TaskRunner:
    """Registers jobs and runs them once, collecting a :class:`RunReport`."""

    def __init__(self, registry: Optional[JobRegistry] = None) -> None:
        self.registry = registry if registry is not None else JobRegistry()

    def add(self, name: str, func: Callable[[], Any], retries: int = 0) -> Job:
        """Register a job and return it."""
        job = Job(name=name, func=func, retries=retries)
        self.registry.add(job)
        return job

    def run(self) -> RunReport:
        """Run every registered job and return the report."""
        report = RunReport()
        for job in self.registry.execution_order():
            report.results.append(self.run_job(job))
        return report

    def run_job(self, job: Job) -> JobResult:
        """Run one job, retrying on exceptions up to ``job.retries`` times."""
        attempts = 0
        last_error = None
        while attempts <= job.retries:
            attempts += 1
            try:
                value = job.func()
            except Exception as exc:
                last_error = f"{type(exc).__name__}: {exc}"
            else:
                return JobResult(
                    job.name, JobStatus.SUCCESS, value=value, attempts=attempts
                )
        return JobResult(
            job.name, JobStatus.FAILED, error=last_error, attempts=attempts
        )
