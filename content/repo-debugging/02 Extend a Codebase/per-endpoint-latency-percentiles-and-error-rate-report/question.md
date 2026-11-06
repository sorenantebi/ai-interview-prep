---
difficulty: Medium
kind: extend
---
# Per-endpoint latency percentiles and error-rate report

**Kind:** Extend the codebase · **Difficulty:** Medium

## Scenario
`logstats` is a small library our on-call engineers use to analyse web-server access logs. Today it can parse log lines, count requests per endpoint, compute mean latency and print a traffic report. Mean latency hides tail behaviour, and nobody can see which endpoints are failing most often. Your ticket: add per-endpoint p50/p95/p99 latency and an error-rate report that lists the worst endpoint first.

## Your tasks
1. Add a `percentile(values, pct)` function to `logstats/stats.py` using the **nearest-rank** method: sort the values, take the value at 1-based rank `ceil(pct / 100 * n)`. `pct=0` returns the minimum and `pct=100` the maximum. Raise `ValueError` for an empty list or a `pct` outside 0-100. The input list must not be modified.
2. Add `LogAnalyzer.latency_percentiles(endpoint)` in `logstats/analyzer.py`. It returns a dict `{"p50": ..., "p95": ..., "p99": ...}` for that endpoint. An unknown endpoint raises `KeyError`, like the existing `mean_latency`.
3. Add `LogAnalyzer.error_rates(min_requests=1)`. It returns a list of `ErrorRate` rows (already defined in `logstats/models.py`), one per endpoint with at least `min_requests` requests. Sort them worst first: highest error rate, then most errors, then endpoint name A-Z. Only server errors count as errors (see `LogEntry.is_error`).
4. Add `format_error_report(analyzer, min_requests=1)` in `logstats/report.py`. The first line is `Error rate report`, followed by one line per row in the form `<endpoint> <errors>/<requests> <rate>%`, with the rate as a percentage to one decimal place (for example `GET /api/search 1/4 25.0%`). If there are no rows, the second line is `No requests.`.

## Notes
- Endpoints are identified as `"<METHOD> <normalised path>"` (see `LogEntry.endpoint`). Reuse the existing helpers instead of re-implementing grouping or normalisation.
- The existing tests pass today and must keep passing. The new feature tests in `tests/` fail until you build the feature.
- Entry points: `logstats.parser.parse_lines` turns raw lines into entries, `LogAnalyzer` aggregates them, and `logstats.report` formats the output.
- Run runs the tests in `tests/`; Submit runs them plus hidden tests. You may use the AI assistant panel like you would in an AI-enabled interview: it can read every file but can't edit them.
