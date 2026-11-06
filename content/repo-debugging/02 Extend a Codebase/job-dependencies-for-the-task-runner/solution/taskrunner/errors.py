"""Exceptions raised by the task runner."""


class TaskRunnerError(Exception):
    """Base class for all errors raised by the task runner."""


class DuplicateJobError(TaskRunnerError):
    """Raised when a job name is registered twice."""

    def __init__(self, name):
        super().__init__(f"job already registered: {name!r}")
        self.name = name


class UnknownJobError(TaskRunnerError):
    """Raised when a job name is not known to the registry."""

    def __init__(self, name):
        super().__init__(f"unknown job: {name!r}")
        self.name = name


class CycleError(TaskRunnerError):
    """Raised when job dependencies contain a cycle.

    ``cycle`` is a closed list of names (first == last); each name depends on
    the one that follows it.
    """

    def __init__(self, cycle):
        self.cycle = list(cycle)
        super().__init__("dependency cycle: " + " -> ".join(self.cycle))
