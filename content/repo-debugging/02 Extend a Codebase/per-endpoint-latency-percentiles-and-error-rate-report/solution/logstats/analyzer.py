"""Aggregation of parsed log entries per endpoint."""

from collections import Counter, defaultdict

from . import stats
from .models import ErrorRate


class LogAnalyzer:
    """Collects :class:`~logstats.models.LogEntry` objects and summarises them."""

    def __init__(self, entries=()):
        self._by_endpoint = defaultdict(list)
        self._status_counts = Counter()
        self._total = 0
        for entry in entries:
            self.add(entry)

    def add(self, entry):
        """Register one entry."""
        self._by_endpoint[entry.endpoint].append(entry)
        self._status_counts[entry.status] += 1
        self._total += 1

    def __len__(self):
        return self._total

    def endpoints(self):
        """All known endpoints, sorted alphabetically."""
        return sorted(self._by_endpoint)

    def entries_for(self, endpoint):
        """A copy of the entries recorded for ``endpoint``."""
        return list(self._by_endpoint.get(endpoint, ()))

    def request_counts(self):
        """Mapping of endpoint to number of requests."""
        return {ep: len(items) for ep, items in self._by_endpoint.items()}

    def status_counts(self):
        """Mapping of HTTP status code to number of responses."""
        return dict(self._status_counts)

    def _latencies(self, endpoint):
        items = self._by_endpoint.get(endpoint)
        if not items:
            raise KeyError(endpoint)
        return [entry.latency_ms for entry in items]

    def mean_latency(self, endpoint):
        """Mean latency in milliseconds for ``endpoint``."""
        return stats.mean(self._latencies(endpoint))

    def latency_percentiles(self, endpoint):
        """p50, p95 and p99 latency (ms) for ``endpoint``."""
        latencies = sorted(self._latencies(endpoint))
        return {
            "p50": stats.percentile(latencies, 50),
            "p95": stats.percentile(latencies, 95),
            "p99": stats.percentile(latencies, 99),
        }

    def error_rates(self, min_requests=1):
        """Per-endpoint error rates, worst endpoint first.

        Endpoints with fewer than ``min_requests`` requests are left out. Rows
        are ordered by error rate, then error count (both descending), then
        endpoint name.
        """
        rows = []
        for endpoint, items in self._by_endpoint.items():
            total = len(items)
            if total < min_requests:
                continue
            errors = sum(1 for entry in items if entry.is_error)
            rows.append(ErrorRate(endpoint, total, errors, errors / total))
        rows.sort(key=lambda row: (-row.rate, -row.errors, row.endpoint))
        return rows
