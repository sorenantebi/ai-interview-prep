from datetime import date

from scheduler import filters
from scheduler.formatting import format_agenda
from scheduler.models import Event


def test_upcoming_excludes_past():
    events = [Event("Old", "1/1/2025"), Event("New", "1/6/2025")]
    result = filters.upcoming(events, date(2025, 3, 1))
    assert [event.title for event in result] == ["New"]


def test_in_range_is_inclusive():
    events = [
        Event("Before", "28/2/2025"),
        Event("Start", "1/3/2025"),
        Event("End", "31/3/2025"),
        Event("After", "1/4/2025"),
    ]
    result = filters.in_range(events, date(2025, 3, 1), date(2025, 3, 31))
    assert [event.title for event in result] == ["Start", "End"]


def test_by_category_case_insensitive():
    events = [Event("A", "1/1/2025", category="Social"), Event("B", "2/1/2025")]
    result = filters.by_category(events, "social")
    assert [event.title for event in result] == ["A"]


def test_tags_are_per_event():
    first = Event("First", "1/1/2025")
    second = Event("Second", "2/1/2025")
    first.add_tag("urgent")
    assert first.has_tag("urgent")
    assert not second.has_tag("urgent"), second.tags
    result = filters.with_tag([first, second], "urgent")
    assert [event.title for event in result] == ["First"]


def test_format_agenda():
    events = [Event("Demo", "05/03/2025", category="work")]
    assert format_agenda(events) == "5/3/2025 - Demo (work)"
    assert format_agenda([]) == "No events."
