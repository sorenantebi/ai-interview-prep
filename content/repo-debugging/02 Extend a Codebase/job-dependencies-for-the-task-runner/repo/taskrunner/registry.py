"""Registry that stores jobs and decides in which order they run."""

from typing import Dict, List

from taskrunner.errors import DuplicateJobError, UnknownJobError
from taskrunner.models import Job


class JobRegistry:
    """Keeps jobs by name, remembering the order they were added in."""

    def __init__(self) -> None:
        self._jobs: Dict[str, Job] = {}

    def add(self, job: Job) -> None:
        if job.name in self._jobs:
            raise DuplicateJobError(job.name)
        self._jobs[job.name] = job

    def get(self, name: str) -> Job:
        try:
            return self._jobs[name]
        except KeyError:
            raise UnknownJobError(name) from None

    def names(self) -> List[str]:
        """Job names in insertion order."""
        return list(self._jobs)

    def __len__(self) -> int:
        return len(self._jobs)

    def __contains__(self, name: object) -> bool:
        return name in self._jobs

    def execution_order(self) -> List[Job]:
        """Return the jobs in the order they should run."""
        return list(self._jobs.values())
