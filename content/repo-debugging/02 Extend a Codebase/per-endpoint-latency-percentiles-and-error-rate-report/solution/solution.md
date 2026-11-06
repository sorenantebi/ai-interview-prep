# Per-endpoint latency percentiles and error-rate report - Solution

## Root causes / approach
This is a feature task, so nothing is broken. The work is to build the feature in the layers the codebase already has.

- **`logstats/stats.py`: `percentile`.** It validates `pct` (0-100), sorts a copy of the input with `sorted()` (so the caller's list is untouched) and raises `ValueError` for empty input. It then picks rank `ceil(pct * n / 100)`, clamped to at least 1 so that `pct=0` returns the minimum. Multiplying before dividing keeps integer percentiles exact. For example, `95 * 20 / 100` is exactly `19.0`, whereas going through `0.95` could push the rank up by one.
- **`logstats/analyzer.py`: `latency_percentiles`.** It reuses `_latencies`, which already raises `KeyError` for unknown endpoints and is shared with `mean_latency`. It sorts once and then asks `stats.percentile` for 50, 95 and 99. Sorting an already sorted list is cheap, which keeps the cost at O(n log n) for one call instead of three independent sorts of unsorted data. The analyzer keeps no cached results, so entries added later are picked up.
- **`logstats/analyzer.py`: `error_rates`.** It walks `_by_endpoint` once, which is O(n) overall. It counts errors via `LogEntry.is_error` (5xx only; 4xx are deliberately excluded), builds `ErrorRate` rows with true division, filters by `min_requests`, and sorts with the key `(-rate, -errors, endpoint)`. Negating the numbers gives "worst first" while keeping the name ascending in the same sort.
- **`logstats/report.py`: `format_error_report`.** It formats the rows from `error_rates` and mirrors the structure of `format_traffic_report` (header, `No requests.` for an empty result, one line per row). The rate is `rate * 100` with one decimal place.

Common mistakes: using the average of the two middle values (that is not nearest rank), using integer division for the rate, counting 4xx as errors, sorting the stored entries in place, and forgetting that the empty report still needs the `No requests.` line.

## How to find it
1. Run the tests. `tests/test_stats.py`, `tests/test_analyzer.py` and `tests/test_report.py` show which pieces are missing (`stats.percentile`, `latency_percentiles`, `error_rates`, `format_error_report`).
2. Read `analyzer.py` and `models.py` first. `_latencies`, `ErrorRate` and `LogEntry.is_error` already exist, so the new code should reuse them instead of re-grouping the entries.
3. Read `report.format_traffic_report` as the template for the output format, then build bottom-up: `stats.percentile`, then the analyzer methods, then the report.
4. Check the tie-break rules and the 4xx handling against `_error_fixture` in `tests/test_analyzer.py`, which contains deliberate ties and a 404.
