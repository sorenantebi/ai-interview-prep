"""Plain-text reports built on top of :class:`LogAnalyzer`."""


def format_traffic_report(analyzer, limit=5):
    """List the busiest endpoints, most requests first (ties A-Z)."""
    counts = analyzer.request_counts()
    ranked = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    lines = ["Traffic report"]
    if not ranked:
        lines.append("No requests.")
    for endpoint, count in ranked[:limit]:
        lines.append(f"{endpoint} {count}")
    return "\n".join(lines)


def format_error_report(analyzer, min_requests=1):
    """List endpoints by error rate, worst first."""
    rows = analyzer.error_rates(min_requests)
    lines = ["Error rate report"]
    if not rows:
        lines.append("No requests.")
    for row in rows:
        lines.append(f"{row.endpoint} {row.errors}/{row.requests} {row.rate * 100:.1f}%")
    return "\n".join(lines)
