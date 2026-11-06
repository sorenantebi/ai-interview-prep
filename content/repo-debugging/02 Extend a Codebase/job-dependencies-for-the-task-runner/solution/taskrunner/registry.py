"""Registry that stores jobs and decides in which order they run."""

import heapq
from collections import defaultdict
from typing import Dict, List

from taskrunner.errors import CycleError, DuplicateJobError, UnknownJobError
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
        """Return the jobs in the order they should run.

        Every job comes after all of its dependencies. Among the jobs that are
        ready, the one added first is scheduled first. Raises
        :class:`UnknownJobError` for a dependency that was never added and
        :class:`CycleError` if the dependencies contain a cycle.
        """
        names = list(self._jobs)
        index = {name: i for i, name in enumerate(names)}
        pending = {}
        dependents = defaultdict(list)
        for name, job in self._jobs.items():
            deps = list(dict.fromkeys(job.depends_on))
            for dep in deps:
                if dep not in self._jobs:
                    raise UnknownJobError(dep)
                dependents[dep].append(name)
            pending[name] = len(deps)

        ready = [index[name] for name, count in pending.items() if count == 0]
        heapq.heapify(ready)
        order: List[Job] = []
        while ready:
            name = names[heapq.heappop(ready)]
            order.append(self._jobs[name])
            for child in dependents[name]:
                pending[child] -= 1
                if pending[child] == 0:
                    heapq.heappush(ready, index[child])

        if len(order) != len(names):
            unresolved = {name for name, count in pending.items() if count > 0}
            raise CycleError(self._find_cycle(unresolved, index))
        return order

    def _find_cycle(self, unresolved, index) -> List[str]:
        """Extract one real cycle from the jobs that could not be scheduled.

        Every unresolved job has at least one unresolved dependency, so
        following such dependencies from any unresolved job must eventually
        revisit a job; the part of the walk from that job on is a cycle.
        """
        start = min(unresolved, key=index.__getitem__)
        path: List[str] = []
        position = {}
        node = start
        while node not in position:
            position[node] = len(path)
            path.append(node)
            node = next(
                dep for dep in self._jobs[node].depends_on if dep in unresolved
            )
        cycle = path[position[node]:]
        first = min(range(len(cycle)), key=lambda i: index[cycle[i]])
        cycle = cycle[first:] + cycle[:first]
        cycle.append(cycle[0])
        return cycle
