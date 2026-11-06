import random
import time

from logstats import stats
from logstats.analyzer import LogAnalyzer
from logstats.models import LogEntry
from logstats.parser import parse_lines
from logstats.report import format_error_report


def make(method, path, status=200, latency=10.0):
    return LogEntry("2024-03-01T12:00:00Z", method, path, status, latency)


def test_percentile_single_value():
    for pct in (0, 1, 50, 99, 100):
        assert stats.percentile([7], pct) == 7


def test_percentile_bounds():
    values = [5, 3, 9, 1, 7]
    assert stats.percentile(values, 0) == 1
    assert stats.percentile(values, 100) == 9


def test_percentile_duplicates_and_floats():
    assert stats.percentile([2.5, 2.5, 2.5, 9.0], 50) == 2.5
    assert stats.percentile([1.5, 0.5, 2.5], 100) == 2.5


def test_percentile_rank_rounds_up():
    values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    assert stats.percentile(values, 91) == 10
    assert stats.percentile(values, 90) == 9
    assert stats.percentile(values, 10) == 1
    assert stats.percentile(values, 11) == 2


def test_percentile_accepts_tuple_and_does_not_mutate_list():
    assert stats.percentile((3, 1, 2), 50) == 2
    values = [3, 1, 2]
    stats.percentile(values, 99)
    assert values == [3, 1, 2]


def test_latency_percentiles_keys_and_single_sample():
    analyzer = LogAnalyzer([make("GET", "/a", latency=42.0)])
    assert analyzer.latency_percentiles("GET /a") == {"p50": 42.0, "p95": 42.0, "p99": 42.0}


def test_latency_percentiles_reflect_entries_added_later():
    analyzer = LogAnalyzer([make("GET", "/a", latency=1.0)])
    assert analyzer.latency_percentiles("GET /a")["p99"] == 1.0
    analyzer.add(make("GET", "/a", latency=500.0))
    assert analyzer.latency_percentiles("GET /a")["p99"] == 500.0


def test_latency_percentiles_do_not_reorder_stored_entries():
    analyzer = LogAnalyzer([make("GET", "/a", latency=l) for l in (30.0, 10.0, 20.0)])
    analyzer.latency_percentiles("GET /a")
    assert [e.latency_ms for e in analyzer.entries_for("GET /a")] == [30.0, 10.0, 20.0]


def test_latency_percentiles_are_per_endpoint():
    analyzer = LogAnalyzer(
        [make("GET", "/fast", latency=1.0)] * 5 + [make("GET", "/slow", latency=900.0)] * 5
    )
    assert analyzer.latency_percentiles("GET /fast")["p99"] == 1.0
    assert analyzer.latency_percentiles("GET /slow")["p50"] == 900.0


def test_error_rates_empty_analyzer():
    assert LogAnalyzer().error_rates() == []


def test_error_rate_is_true_division():
    analyzer = LogAnalyzer([make("GET", "/a", 500), make("GET", "/a"), make("GET", "/a")])
    rows = analyzer.error_rates()
    assert abs(rows[0].rate - 1 / 3) < 1e-12


def test_client_errors_are_not_counted():
    analyzer = LogAnalyzer([make("GET", "/a", 404), make("GET", "/a", 429), make("GET", "/a", 200)])
    row = analyzer.error_rates()[0]
    assert row.errors == 0 and row.rate == 0.0


def test_error_rates_tie_breaks_on_errors_then_name():
    entries = []
    entries += [make("GET", "/z", 500)] * 2 + [make("GET", "/z")] * 2  # 2/4
    entries += [make("GET", "/a", 500)] + [make("GET", "/a")]  # 1/2
    entries += [make("GET", "/b", 500)] + [make("GET", "/b")]  # 1/2
    rows = LogAnalyzer(entries).error_rates()
    assert [r.endpoint for r in rows] == ["GET /z", "GET /a", "GET /b"]


def test_error_rates_min_requests_excludes_all():
    analyzer = LogAnalyzer([make("GET", "/a", 500)])
    assert analyzer.error_rates(min_requests=2) == []


def test_error_report_empty_and_rounding():
    assert format_error_report(LogAnalyzer()) == "Error rate report\nNo requests."
    analyzer = LogAnalyzer([make("GET", "/a", 500), make("GET", "/a"), make("GET", "/a")])
    assert format_error_report(analyzer) == "Error rate report\nGET /a 1/3 33.3%"


def test_error_report_min_requests():
    analyzer = LogAnalyzer([make("GET", "/a", 500), make("GET", "/b", 500), make("GET", "/b")])
    assert format_error_report(analyzer, min_requests=2) == "Error rate report\nGET /b 1/2 50.0%"


def test_end_to_end_from_raw_lines():
    lines = [
        "2024-03-01T12:00:00Z GET /api/users/1 200 10ms",
        "2024-03-01T12:00:01Z GET /api/users/2 500 30ms",
        "2024-03-01T12:00:02Z GET /api/users/3/ 200 20ms",
        "broken line",
        "2024-03-01T12:00:03Z get /api/users/4?x=1 200 40ms",
    ]
    entries, skipped = parse_lines(lines)
    assert skipped == 1
    analyzer = LogAnalyzer(entries)
    assert analyzer.latency_percentiles("GET /api/users/:id") == {"p50": 20.0, "p95": 40.0, "p99": 40.0}
    assert format_error_report(analyzer) == "Error rate report\nGET /api/users/:id 1/4 25.0%"


def test_large_input_is_fast():
    rng = random.Random(0)
    entries = [
        make("GET", f"/api/items/{i}", 500 if rng.random() < 0.05 else 200, rng.random() * 1000)
        for i in range(100_000)
    ]
    analyzer = LogAnalyzer(entries)
    start = time.perf_counter()
    result = analyzer.latency_percentiles("GET /api/items/:id")
    rows = analyzer.error_rates()
    elapsed = time.perf_counter() - start
    assert result["p50"] <= result["p95"] <= result["p99"]
    assert len(rows) == 1
    assert elapsed < 1.0, f"took {elapsed:.2f}s"
