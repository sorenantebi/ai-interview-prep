"""Formatting helpers for reports."""

from taskrunner.models import JobResult, RunReport


def format_result(result: JobResult) -> str:
    """One human-readable line for a single result."""
    line = f"{result.name}: {result.status.value}"
    if result.attempts > 1:
        line += f" (attempts: {result.attempts})"
    if result.error:
        line += f" - {result.error}"
    return line


def format_report(report: RunReport) -> str:
    """Multi-line summary of a run, one line per job."""
    return "\n".join(format_result(r) for r in report.results)
