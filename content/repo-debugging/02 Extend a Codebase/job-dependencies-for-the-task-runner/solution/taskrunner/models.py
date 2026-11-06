"""Data classes shared by the registry, the runner and the formatters."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, List, Optional, Tuple

from taskrunner.errors import UnknownJobError


class JobStatus(Enum):
    """Final state of a job after a run."""

    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass(frozen=True)
class Job:
    """A unit of work.

    ``func`` is called without arguments. ``retries`` is the number of
    additional attempts after the first one fails. ``depends_on`` lists the
    names of jobs that must succeed before this one runs.
    """

    name: str
    func: Callable[[], Any]
    retries: int = 0
    depends_on: Tuple[str, ...] = ()


@dataclass
class JobResult:
    """Outcome of a single job."""

    name: str
    status: JobStatus
    value: Any = None
    error: Optional[str] = None
    attempts: int = 0


@dataclass
class RunReport:
    """Results of one run, in the order the jobs were handled."""

    results: List[JobResult] = field(default_factory=list)

    def get(self, name: str) -> JobResult:
        for result in self.results:
            if result.name == name:
                return result
        raise UnknownJobError(name)

    def _names_with(self, status: JobStatus) -> List[str]:
        return [r.name for r in self.results if r.status is status]

    @property
    def succeeded(self) -> List[str]:
        return self._names_with(JobStatus.SUCCESS)

    @property
    def failed(self) -> List[str]:
        return self._names_with(JobStatus.FAILED)

    @property
    def skipped(self) -> List[str]:
        return self._names_with(JobStatus.SKIPPED)

    @property
    def ok(self) -> bool:
        return all(r.status is JobStatus.SUCCESS for r in self.results)
