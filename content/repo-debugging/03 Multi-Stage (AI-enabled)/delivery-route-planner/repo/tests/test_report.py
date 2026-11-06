from routeplanner.models import Route
from routeplanner.report import describe_route, format_duration


def test_format_duration_minutes_and_hours():
    assert format_duration(45) == "45m"
    assert format_duration(65) == "1h 05m"
    assert format_duration(120) == "2h 00m"


def test_format_duration_zero():
    assert format_duration(0) == "0m"


def test_describe_route():
    route = Route(65.0, ("A", "B", "C"))
    assert describe_route(route) == "A -> B -> C (1h 05m)"
