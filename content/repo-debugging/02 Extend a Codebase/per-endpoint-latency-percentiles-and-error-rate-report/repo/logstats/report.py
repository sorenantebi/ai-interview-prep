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
