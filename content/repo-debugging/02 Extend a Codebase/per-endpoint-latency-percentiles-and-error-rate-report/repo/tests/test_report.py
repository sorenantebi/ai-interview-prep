from logstats.analyzer import LogAnalyzer
from logstats.models import LogEntry
from logstats.report import format_error_report, format_traffic_report


def make(method, path, status=200):
    return LogEntry("2024-03-01T12:00:00Z", method, path, status, 5.0)


def test_traffic_report_orders_by_count():
    analyzer = LogAnalyzer([make("GET", "/b")] + [make("GET", "/a")] * 2 + [make("GET", "/c")])
    text = format_traffic_report(analyzer, limit=2)
    assert text == "Traffic report\nGET /a 2\nGET /b 1"


def test_traffic_report_empty():
    assert format_traffic_report(LogAnalyzer()) == "Traffic report\nNo requests."


def test_error_report_format():
    entries = [make("GET", "/api/users/1", 500)] + [make("GET", "/api/users/2")] * 3
    entries += [make("POST", "/api/orders", 500), make("POST", "/api/orders", 503)]
    entries += [make("GET", "/health")] * 10
    text = format_error_report(LogAnalyzer(entries))
    assert text == (
        "Error rate report\n"
        "POST /api/orders 2/2 100.0%\n"
        "GET /api/users/:id 1/4 25.0%\n"
        "GET /health 0/10 0.0%"
    )
