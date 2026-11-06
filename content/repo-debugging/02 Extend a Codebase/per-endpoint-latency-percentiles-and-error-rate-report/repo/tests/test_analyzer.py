from logstats.analyzer import LogAnalyzer
from logstats.models import LogEntry


def make(method, path, status=200, latency=10.0):
    return LogEntry("2024-03-01T12:00:00Z", method, path, status, latency)


def test_endpoint_normalisation_groups_ids():
    analyzer = LogAnalyzer(
        [make("GET", "/api/users/1"), make("GET", "/api/users/2?x=1"), make("GET", "/health")]
    )
    assert analyzer.endpoints() == ["GET /api/users/:id", "GET /health"]
    assert analyzer.request_counts()["GET /api/users/:id"] == 2


def test_status_counts_and_len():
    analyzer = LogAnalyzer([make("GET", "/a", 200), make("GET", "/a", 500), make("GET", "/b", 200)])
    assert len(analyzer) == 3
    assert analyzer.status_counts() == {200: 2, 500: 1}


def test_mean_latency_and_unknown_endpoint():
    analyzer = LogAnalyzer([make("GET", "/a", latency=10), make("GET", "/a", latency=30)])
    assert analyzer.mean_latency("GET /a") == 20.0
    try:
        analyzer.mean_latency("GET /missing")
    except KeyError:
        pass
    else:
        assert False, "expected KeyError"


def test_latency_percentiles():
    entries = [make("GET", f"/api/users/{i}", latency=10.0 * i) for i in range(1, 21)]
    analyzer = LogAnalyzer(entries)
    result = analyzer.latency_percentiles("GET /api/users/:id")
    assert result == {"p50": 100.0, "p95": 190.0, "p99": 200.0}


def test_latency_percentiles_unknown_endpoint():
    analyzer = LogAnalyzer([make("GET", "/a")])
    try:
        analyzer.latency_percentiles("GET /nope")
    except KeyError:
        pass
    else:
        assert False, "expected KeyError"


def _error_fixture():
    entries = []
    entries += [make("GET", "/api/users/1", 500)] + [make("GET", "/api/users/2")] * 3
    entries += [make("POST", "/api/orders", 500), make("POST", "/api/orders", 503)]
    entries += [make("GET", "/health")] * 10
    entries += [make("GET", "/api/search", 500), make("GET", "/api/search", 404)]
    entries += [make("GET", "/api/search")] * 2
    return LogAnalyzer(entries)


def test_error_rates_sorted_worst_first():
    rows = _error_fixture().error_rates()
    assert [r.endpoint for r in rows] == [
        "POST /api/orders",
        "GET /api/search",
        "GET /api/users/:id",
        "GET /health",
    ]
    assert rows[0].rate == 1.0
    assert rows[1].requests == 4 and rows[1].errors == 1 and rows[1].rate == 0.25


def test_error_rates_min_requests():
    rows = _error_fixture().error_rates(min_requests=3)
    assert [r.endpoint for r in rows] == [
        "GET /api/search",
        "GET /api/users/:id",
        "GET /health",
    ]
