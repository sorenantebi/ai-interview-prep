"""Human readable output for dispatchers."""


def format_duration(minutes):
    """Format minutes as ``'45m'`` or ``'1h 05m'`` (rounded to whole minutes)."""
    total = int(round(minutes))
    hours, mins = divmod(total, 60)
    if hours:
        return f"{hours}h {mins:02d}m"
    return f"{mins}m"


def describe_route(route):
    """One-line summary such as ``'A -> B -> C (1h 05m)'``."""
    return " -> ".join(route.path) + f" ({format_duration(route.minutes)})"
