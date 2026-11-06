from datetime import date

from scheduler import filters
from scheduler.formatting import format_agenda
from scheduler.models import Event
from scheduler.service import Scheduler


def build(*pairs):
    scheduler = Scheduler()
    for title, day in pairs:
        scheduler.add(Event(title, day))
    return scheduler


def titles(events):
    return [event.title for event in events]


def test_sort_across_years():
    s = build(("c", "1/1/2026"), ("a", "31/12/2024"), ("b", "15/6/2025"))
    assert titles(s.sorted_events()) == ["a", "b", "c"]


def test_sort_day_numeric_not_lexical():
    s = build(("x", "2/1/2025"), ("y", "10/1/2025"), ("z", "1/1/2025"))
    assert titles(s.sorted_events()) == ["z", "x", "y"]


def test_sort_mixed_padding():
    s = build(("late", "05/03/2025"), ("early", "4/3/2025"))
    assert titles(s.sorted_events()) == ["early", "late"]


def test_sort_ties_by_title_case_insensitive():
    s = build(("beta", "1/1/2025"), ("Alpha", "1/1/2025"))
    assert titles(s.sorted_events()) == ["Alpha", "beta"]


def test_sort_reverse():
    s = build(("a", "9/1/2025"), ("b", "10/1/2025"), ("c", "2/12/2024"))
    assert titles(s.sorted_events(reverse=True)) == ["b", "a", "c"]


def test_upcoming_today_only():
    s = build(("today", "10/3/2025"))
    assert titles(s.upcoming(today=date(2025, 3, 10))) == ["today"]


def test_upcoming_year_boundary_sorted():
    s = build(
        ("new year", "1/1/2025"),
        ("eve", "31/12/2024"),
        ("past", "30/12/2024"),
    )
    result = s.upcoming(today=date(2024, 12, 31))
    assert titles(result) == ["eve", "new year"]


def test_upcoming_limit_zero_and_large():
    s = build(("a", "10/3/2025"), ("b", "11/3/2025"))
    assert s.upcoming(today=date(2025, 3, 10), limit=0) == []
    assert len(s.upcoming(today=date(2025, 3, 10), limit=10)) == 2


def test_upcoming_default_today():
    s = build(("old", "1/1/2000"), ("far", "1/1/2999"))
    assert titles(s.upcoming()) == ["far"]


def test_agenda_text():
    s = build(("Demo", "10/3/2025"), ("Review", "9/3/2025"))
    text = s.agenda(today=date(2025, 3, 10))
    assert text == "10/3/2025 - Demo (general)"
    assert s.agenda(today=date(2030, 1, 1)) == "No events."


def test_tags_default_independent():
    a = Event("a", "1/1/2025")
    b = Event("b", "1/1/2025")
    a.add_tag("x")
    a.add_tag("x")
    assert a.tags == ["x"]
    assert b.tags == []


def test_tags_input_not_aliased():
    shared = ["base"]
    e = Event("a", "1/1/2025", tags=shared)
    e.add_tag("extra")
    assert shared == ["base"]
    assert e.tags == ["base", "extra"]


def test_tagged_query():
    s = build(("a", "10/1/2025"), ("b", "2/1/2025"), ("c", "3/1/2025"))
    events = s.sorted_events()
    for event in events:
        if event.title != "c":
            event.add_tag("t")
    assert titles(s.tagged("t")) == ["b", "a"]


def test_between_inclusive_and_sorted():
    s = build(
        ("a", "10/3/2025"),
        ("b", "1/3/2025"),
        ("c", "31/3/2025"),
        ("d", "1/4/2025"),
        ("e", "28/2/2025"),
    )
    result = s.between(date(2025, 3, 1), date(2025, 3, 31))
    assert titles(result) == ["b", "a", "c"]


def test_remove_missing_and_duplicates():
    s = build(("a", "1/1/2025"), ("a", "2/1/2025"), ("b", "3/1/2025"))
    assert s.remove("zzz") == 0
    assert s.remove("a") == 2
    assert len(s) == 1


def test_filters_upcoming_boundary():
    events = [Event("t", "10/3/2025"), Event("y", "9/3/2025")]
    assert titles(filters.upcoming(events, date(2025, 3, 10))) == ["t"]


def test_format_agenda_multiple_lines():
    events = [Event("A", "1/2/2025", "x"), Event("B", "03/02/2025", "y")]
    assert format_agenda(events) == "1/2/2025 - A (x)\n3/2/2025 - B (y)"
