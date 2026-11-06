"""Data types used by the analyzer."""

from dataclasses import dataclass
from typing import NamedTuple

from .utils import normalize_path


@dataclass(frozen=True)
class LogEntry:
    """A single parsed access-log line."""

    timestamp: str
    method: str
    path: str
    status: int
    latency_ms: float

    @property
    def endpoint(self):
        """Grouping key: HTTP method plus the normalised path."""
        return f"{self.method} {normalize_path(self.path)}"

    @property
    def is_error(self):
        """True for server errors (5xx). Client errors (4xx) do not count."""
        return self.status >= 500


class ErrorRate(NamedTuple):
    """Error statistics for one endpoint."""

    endpoint: str
    requests: int
    errors: int
    rate: float
