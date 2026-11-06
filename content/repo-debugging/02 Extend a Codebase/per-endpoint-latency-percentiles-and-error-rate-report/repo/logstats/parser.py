"""Parsing of raw access-log lines.

Expected line format::

    2024-03-01T12:00:00Z GET /api/users/42 200 35ms
"""

from .models import LogEntry


class ParseError(ValueError):
    """Raised when a log line does not match the expected format."""


def parse_line(line):
    """Parse one log line into a :class:`LogEntry`."""
    parts = line.split()
    if len(parts) != 5:
        raise ParseError(f"expected 5 fields, got {len(parts)}: {line!r}")
    timestamp, method, path, status, latency = parts
    if not latency.endswith("ms"):
        raise ParseError(f"latency must end with 'ms': {latency!r}")
    try:
        status_code = int(status)
        latency_ms = float(latency[:-2])
    except ValueError as exc:
        raise ParseError(f"invalid number in line: {line!r}") from exc
    return LogEntry(timestamp, method.upper(), path, status_code, latency_ms)


def parse_lines(lines):
    """Parse many lines, skipping blanks and counting malformed ones.

    Returns a ``(entries, skipped)`` tuple.
    """
    entries = []
    skipped = 0
    for line in lines:
        if not line.strip():
            continue
        try:
            entries.append(parse_line(line))
        except ParseError:
            skipped += 1
    return entries, skipped
