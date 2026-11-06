from logstats.parser import ParseError, parse_line, parse_lines


def test_parse_line_basic():
    entry = parse_line("2024-03-01T12:00:00Z GET /api/users/42 200 35ms")
    assert entry.method == "GET"
    assert entry.path == "/api/users/42"
    assert entry.status == 200
    assert entry.latency_ms == 35.0


def test_parse_line_uppercases_method_and_reads_float_latency():
    entry = parse_line("2024-03-01T12:00:01Z post /api/orders 201 12.5ms")
    assert entry.method == "POST"
    assert entry.latency_ms == 12.5


def test_parse_line_rejects_bad_lines():
    for line in ("garbage", "a GET /x 200 35", "a GET /x abc 35ms"):
        try:
            parse_line(line)
        except ParseError:
            continue
        assert False, f"expected ParseError for {line!r}"


def test_parse_lines_skips_blank_and_counts_malformed():
    lines = [
        "2024-03-01T12:00:00Z GET /health 200 1ms",
        "",
        "not a log line",
        "2024-03-01T12:00:02Z GET /health 200 2ms",
    ]
    entries, skipped = parse_lines(lines)
    assert len(entries) == 2
    assert skipped == 1
