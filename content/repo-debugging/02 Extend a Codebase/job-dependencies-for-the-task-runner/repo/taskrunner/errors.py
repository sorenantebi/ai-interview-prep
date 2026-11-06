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
